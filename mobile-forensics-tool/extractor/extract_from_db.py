#!/usr/bin/env python3
"""
Database Extractor for Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Extract SMS/MMS from Android mmssms.db
- Extract calls from Android calllog.db
- Extract contacts from Android contacts2.db
- Convert to standardized JSON format
- Maintain forensic chain of custody

INPUT: Raw Android database files
OUTPUT: Processed JSON evidence files
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

def extract_sms_from_db(db_path, output_path):
    """
    Extract SMS/MMS from Android mmssms.db database.
    
    Args:
        db_path: Path to mmssms.db
        output_path: Path to output JSON file
    """
    sms_data = []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query SMS table
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        print(f"Available tables: {[t[0] for t in tables]}")
        
        if ('sms',) in tables:
            cursor.execute("""
                SELECT 
                    date,
                    date_sent,
                    read,
                    status,
                    type,
                    body,
                    address
                FROM sms 
                ORDER BY date
            """)
            
            rows = cursor.fetchall()
            print(f"Found {len(rows)} SMS records")
        else:
            print("SMS table not found")
            rows = []
        
        for row in rows:
            # Convert Android timestamp (milliseconds) to readable format
            timestamp_ms = row[0] if row[0] else row[1]  # Use date_sent if date is null
            if timestamp_ms:
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = "Unknown"
            
            # Determine message type
            msg_type = row[4]  # 1 = inbox, 2 = sent, 3 = draft, 4 = outbox, 5 = failed
            if msg_type == 1:
                msg_type_str = "incoming"
            elif msg_type == 2:
                msg_type_str = "outgoing"
            elif msg_type == 3:
                msg_type_str = "draft"
            elif msg_type == 4:
                msg_type_str = "outbox"
            else:
                msg_type_str = "unknown"
            
            sms_entry = {
                "timestamp": timestamp,
                "source": "SMS",
                "type": msg_type_str,
                "details": f"Message {'from' if msg_type_str == 'incoming' else 'to'} {row[6] or 'Unknown'}: {row[5] or '[No content]'}"
            }
            
            sms_data.append(sms_entry)
        
        conn.close()
        
        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(sms_data, f, indent=2)
        
        print(f"Extracted {len(sms_data)} SMS messages to {output_path}")
        return sms_data
        
    except Exception as e:
        print(f"Error extracting SMS from {db_path}: {e}")
        return []

def extract_calls_from_db(db_path, output_path):
    """
    Extract call logs from Android calllog.db database.
    
    Args:
        db_path: Path to calllog.db
        output_path: Path to output JSON file
    """
    call_data = []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query calls table
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        print(f"Available tables: {[t[0] for t in tables]}")
        
        if ('calls',) in tables:
            cursor.execute("""
                SELECT 
                    date,
                    duration,
                    type,
                    number,
                    name
                FROM calls 
                ORDER BY date
            """)
            
            rows = cursor.fetchall()
            print(f"Found {len(rows)} call records")
        else:
            print("Calls table not found")
            rows = []
        
        for row in rows:
            # Convert Android timestamp to readable format
            timestamp_ms = row[0]
            if timestamp_ms:
                timestamp = datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
            else:
                timestamp = "Unknown"
            
            # Determine call type
            call_type = row[2]  # 1 = incoming, 2 = outgoing, 3 = missed, 5 = voicemail
            if call_type == 1:
                call_type_str = "incoming"
            elif call_type == 2:
                call_type_str = "outgoing"
            elif call_type == 3:
                call_type_str = "missed"
            elif call_type == 5:
                call_type_str = "voicemail"
            else:
                call_type_str = "unknown"
            
            # Format duration
            duration = row[1] if row[1] else 0
            if duration > 0:
                minutes = duration // 60
                seconds = duration % 60
                duration_str = f"{minutes}m {seconds}s"
            else:
                duration_str = "0s"
            
            contact_name = row[4] if row[4] else "Unknown"
            phone_number = row[3] if row[3] else "Unknown"
            
            call_entry = {
                "timestamp": timestamp,
                "source": "CALL",
                "type": call_type_str,
                "details": f"{call_type_str.capitalize()} call {('from' if call_type_str in ['incoming', 'missed'] else 'to')} {contact_name} ({phone_number}) - Duration: {duration_str}"
            }
            
            call_data.append(call_entry)
        
        conn.close()
        
        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(call_data, f, indent=2)
        
        print(f"Extracted {len(call_data)} call logs to {output_path}")
        return call_data
        
    except Exception as e:
        print(f"Error extracting calls from {db_path}: {e}")
        return []

def extract_media_metadata(case_path, output_path):
    """
    Extract metadata from media files.
    
    Args:
        case_path: Path to case directory
        output_path: Path to output JSON file
    """
    media_data = []
    
    try:
        # Look for media files in the case
        media_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.3gp', '.mov']
        
        for ext in media_extensions:
            for media_file in Path(case_path).rglob(f"*{ext}"):
                try:
                    stat = media_file.stat()
                    timestamp = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    
                    media_entry = {
                        "timestamp": timestamp,
                        "source": "MEDIA",
                        "type": "file",
                        "details": f"Media file: {media_file.name} ({stat.st_size} bytes)"
                    }
                    
                    media_data.append(media_entry)
                    
                except Exception as e:
                    print(f"Error processing media file {media_file}: {e}")
        
        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(media_data, f, indent=2)
        
        print(f"Extracted metadata for {len(media_data)} media files to {output_path}")
        return media_data
        
    except Exception as e:
        print(f"Error extracting media metadata: {e}")
        return []

def extract_app_data(case_path, output_path):
    """
    Extract app installation and usage data.
    
    Args:
        case_path: Path to case directory
        output_path: Path to output JSON file
    """
    app_data = []
    
    try:
        # Look for app-related files and directories
        app_indicators = [
            "WhatsApp", "Android", "data", "DCIM"
        ]
        
        for indicator in app_indicators:
            for app_path in Path(case_path).rglob(f"*{indicator}*"):
                if app_path.is_dir():
                    try:
                        stat = app_path.stat()
                        timestamp = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        
                        app_entry = {
                            "timestamp": timestamp,
                            "source": "APP",
                            "type": "data",
                            "details": f"App data directory: {app_path.relative_to(Path(case_path))}"
                        }
                        
                        app_data.append(app_entry)
                        
                    except Exception as e:
                        print(f"Error processing app directory {app_path}: {e}")
        
        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(app_data, f, indent=2)
        
        print(f"Extracted {len(app_data)} app data entries to {output_path}")
        return app_data
        
    except Exception as e:
        print(f"Error extracting app data: {e}")
        return []

def main():
    """Main extraction function for case_002"""
    # Use absolute paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    case_path = os.path.join(base_path, "cases", "case_002", "evidence", "raw")
    output_path = os.path.join(base_path, "cases", "case_002", "evidence", "processed")
    
    print("Mobile Forensics - Database Extraction")
    print("=" * 50)
    print(f"Processing case: case_002")
    print(f"Raw evidence path: {case_path}")
    print(f"Output path: {output_path}")
    print()
    
    # Extract SMS
    sms_db = os.path.join(case_path, "data", "data", "com.android.providers.telephony", "databases", "mmssms.db")
    sms_output = os.path.join(output_path, "sms.json")
    if os.path.exists(sms_db):
        print(f"Found SMS database: {sms_db}")
        extract_sms_from_db(sms_db, sms_output)
    else:
        print(f"SMS database not found: {sms_db}")
    
    # Extract calls
    calls_db = os.path.join(case_path, "data", "data", "com.android.providers.contacts", "databases", "calllog.db")
    calls_output = os.path.join(output_path, "calls.json")
    if os.path.exists(calls_db):
        print(f"Found calls database: {calls_db}")
        extract_calls_from_db(calls_db, calls_output)
    else:
        print(f"Call database not found: {calls_db}")
    
    # Extract media metadata
    media_output = os.path.join(output_path, "media.json")
    extract_media_metadata(case_path, media_output)
    
    # Extract app data
    app_output = os.path.join(output_path, "apps.json")
    extract_app_data(case_path, app_output)
    
    print("\nExtraction completed for case_002")

if __name__ == "__main__":
    main()
