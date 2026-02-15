#!/usr/bin/env python3
"""
Timeline Builder for Live Case - Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Reconstruct chronological timeline from live case evidence sources
- Merge SMS, calls, media, and app events
- Maintain forensic chain of custody
- Generate unified timeline for analysis
"""

import json
import os
from datetime import datetime

def build_live_timeline(case_id="case_live_001"):
    """
    Build unified timeline from all processed evidence for live case.
    
    Args:
        case_id: Case identifier
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_path, "cases", case_id, "evidence", "processed")
    
    timeline_events = []
    
    # Load and merge all evidence types
    evidence_files = {
        "SMS": "sms.json",
        "CALL": "calls.json", 
        "MEDIA": "media.json",
        "APP": "apps.json"
    }
    
    for source_type, filename in evidence_files.items():
        file_path = os.path.join(processed_dir, filename)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    events = json.load(f)
                    
                # Add timeline order counter
                for i, event in enumerate(events):
                    event["timeline_order"] = len(timeline_events) + i + 1
                
                timeline_events.extend(events)
                print(f"Loaded {len(events)} {source_type} events")
                
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"File not found: {filename}")
    
    # Sort timeline chronologically
    try:
        timeline_events.sort(key=lambda x: x.get("timestamp", ""))
        print(f"Sorted {len(timeline_events)} total events chronologically")
    except Exception as e:
        print(f"Error sorting timeline: {e}")
    
    # Update timeline order after sorting
    for i, event in enumerate(timeline_events):
        event["timeline_order"] = i + 1
    
    # Save timeline
    timeline_dir = os.path.join(base_path, "cases", case_id, "timeline")
    os.makedirs(timeline_dir, exist_ok=True)
    
    timeline_file = os.path.join(timeline_dir, "timeline.json")
    with open(timeline_file, 'w') as f:
        json.dump(timeline_events, f, indent=2)
    
    print(f"Timeline saved to: {timeline_file}")
    print(f"Total timeline events: {len(timeline_events)}")
    
    # Print timeline summary
    if timeline_events:
        first_event = timeline_events[0].get("timestamp", "Unknown")
        last_event = timeline_events[-1].get("timestamp", "Unknown")
        print(f"Timeline range: {first_event} to {last_event}")
        
        # Count by source type
        source_counts = {}
        for event in timeline_events:
            source = event.get("source", "Unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
        
        print("Event breakdown:")
        for source, count in source_counts.items():
            print(f"  {source}: {count}")
    
    return timeline_events

if __name__ == "__main__":
    print("Mobile Forensics - Live Case Timeline Builder")
    print("=" * 50)
    
    timeline = build_live_timeline("case_live_001")
    
    print("\nTimeline Summary:")
    print(f"  Total events: {len(timeline)}")
    if timeline:
        print(f"  First event: {timeline[0].get('timestamp', 'Unknown')}")
        print(f"  Last event: {timeline[-1].get('timestamp', 'Unknown')}")
