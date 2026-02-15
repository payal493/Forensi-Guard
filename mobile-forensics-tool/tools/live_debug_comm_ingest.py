#!/usr/bin/env python3
"""
Live Debug Communication Ingestion Tool for Mobile Forensics Investigation Tool

FORENSIC ROLE:
- Process limited communication artifacts for pipeline validation
- Simulates restricted call/SMS access for debugging purposes
- Validates forensic pipeline integrity without system-level extraction
- Maintains forensic transparency and explainability

SECURITY & FORENSIC GUARANTEES:
- This script simulates restricted artifacts for debugging only
- It does NOT bypass Android security or access protected databases
- It is used solely for academic demonstration and pipeline validation
- All artifacts are clearly labeled as debug/demo data
- No real system extraction or security circumvention occurs
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

class LiveDebugCommIngestion:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.case_id = "case_live_001"
        self.raw_dir = self.base_path / "cases" / self.case_id / "evidence" / "raw"
        self.processed_dir = self.base_path / "cases" / self.case_id / "evidence" / "processed"
        
    def ensure_processed_directory(self):
        """Ensure the processed directory exists."""
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Processed directory ready: {self.processed_dir}")
    
    def process_call_log(self):
        """
        Process call log CSV and convert to forensic JSON schema.
        
        FORENSIC TRANSPARENCY:
        This simulates limited call artifacts for debugging purposes.
        It does NOT access protected Android databases or bypass security.
        """
        print("📞 Processing live debug call log...")
        
        call_file = self.raw_dir / "live_debug_calllog.csv"
        output_file = self.processed_dir / "calls.json"
        
        if not call_file.exists():
            print(f"❌ Call log file not found: {call_file}")
            return False
        
        calls = []
        
        try:
            with open(call_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Find header line
                header_line = None
                for i, line in enumerate(lines):
                    if line.startswith('timestamp'):
                        header_line = i
                        break
                
                if header_line is None:
                    print("❌ No header line found in call log")
                    return False
                
                # Parse data from lines after header
                data_lines = lines[header_line + 1:]
                
                for line in data_lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse CSV manually
                    parts = line.split(',')
                    if len(parts) >= 4:
                        timestamp = parts[0].strip()
                        direction = parts[1].strip().lower()
                        number = parts[2].strip()
                        duration = int(parts[3].strip())
                        
                        # Format duration for human readability
                        if duration >= 60:
                            minutes = duration // 60
                            seconds = duration % 60
                            duration_str = f"{minutes}m {seconds}s"
                        else:
                            duration_str = f"{duration}s"
                        
                        # Create forensic entry
                        call_entry = {
                            "timestamp": timestamp,
                            "source": "CALL",
                            "type": direction,
                            "details": f"{direction.capitalize()} call {('from' if direction == 'incoming' else 'to')} {number} - Duration: {duration_str}"
                        }
                        
                        calls.append(call_entry)
            
            # Sort by timestamp
            calls.sort(key=lambda x: x['timestamp'])
            
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(calls, f, indent=2)
            
            print(f"✅ Processed {len(calls)} call entries")
            print(f"✅ Saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error processing call log: {e}")
            return False
    
    def process_sms_log(self):
        """
        Process SMS log CSV and convert to forensic JSON schema.
        
        FORENSIC TRANSPARENCY:
        This simulates limited SMS artifacts for debugging purposes.
        It does NOT access protected Android databases or bypass security.
        """
        print("💬 Processing live debug SMS log...")
        
        sms_file = self.raw_dir / "live_debug_sms.csv"
        output_file = self.processed_dir / "sms.json"
        
        if not sms_file.exists():
            print(f"❌ SMS log file not found: {sms_file}")
            return False
        
        messages = []
        
        try:
            with open(sms_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Find header line
                header_line = None
                for i, line in enumerate(lines):
                    if line.startswith('timestamp'):
                        header_line = i
                        break
                
                if header_line is None:
                    print("❌ No header line found in SMS log")
                    return False
                
                # Parse data from lines after header
                data_lines = lines[header_line + 1:]
                
                for line in data_lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse CSV manually (handle message content with commas)
                    parts = line.split(',')
                    if len(parts) >= 4:
                        timestamp = parts[0].strip()
                        direction = parts[1].strip().lower()
                        number = parts[2].strip()
                        message = ','.join(parts[3:]).strip()  # Handle commas in message
                        
                        # Create forensic entry
                        sms_entry = {
                            "timestamp": timestamp,
                            "source": "SMS",
                            "type": direction,
                            "details": f"Message {('from' if direction == 'incoming' else 'to')} {number}: {message}"
                        }
                        
                        messages.append(sms_entry)
            
            # Sort by timestamp
            messages.sort(key=lambda x: x['timestamp'])
            
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(messages, f, indent=2)
            
            print(f"✅ Processed {len(messages)} SMS entries")
            print(f"✅ Saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error processing SMS log: {e}")
            return False
    
    def validate_pipeline_compatibility(self):
        """Validate that generated files are compatible with existing pipeline."""
        print("🔍 Validating pipeline compatibility...")
        
        calls_file = self.processed_dir / "calls.json"
        sms_file = self.processed_dir / "sms.json"
        
        validation_results = {
            "calls_valid": False,
            "sms_valid": False,
            "schema_compatible": False
        }
        
        try:
            # Validate calls file
            if calls_file.exists():
                with open(calls_file, 'r') as f:
                    calls = json.load(f)
                
                # Check schema compatibility
                if calls and all(key in calls[0] for key in ["timestamp", "source", "type", "details"]):
                    validation_results["calls_valid"] = True
                    print(f"✅ Calls file schema validated ({len(calls)} entries)")
            
            # Validate SMS file
            if sms_file.exists():
                with open(sms_file, 'r') as f:
                    messages = json.load(f)
                
                # Check schema compatibility
                if messages and all(key in messages[0] for key in ["timestamp", "source", "type", "details"]):
                    validation_results["sms_valid"] = True
                    print(f"✅ SMS file schema validated ({len(messages)} entries)")
            
            # Overall compatibility
            validation_results["schema_compatible"] = validation_results["calls_valid"] and validation_results["sms_valid"]
            
            if validation_results["schema_compatible"]:
                print("✅ All files compatible with existing forensic pipeline")
            else:
                print("❌ Schema compatibility issues detected")
                
        except Exception as e:
            print(f"❌ Error validating pipeline compatibility: {e}")
        
        return validation_results
    
    def print_forensic_transparency_notice(self):
        """Print forensic transparency notice."""
        print("\n" + "="*70)
        print("🔒 FORENSIC TRANSPARENCY NOTICE")
        print("="*70)
        print("This tool processes simulated communication artifacts for:")
        print("• Pipeline validation and debugging purposes only")
        print("• Academic demonstration of forensic workflow")
        print("• Testing timeline reconstruction and analysis")
        print("\nIMPORTANT DISCLAIMERS:")
        print("• Does NOT access protected Android databases")
        print("• Does NOT bypass Android security measures")
        print("• Does NOT perform system-level extraction")
        print("• Uses clearly labeled debug/demo data only")
        print("• Maintains full forensic integrity and transparency")
        print("\nAll artifacts are for debugging and should be clearly")
        print("identified as simulated in any forensic reporting.")
        print("="*70)
    
    def print_summary(self, validation_results):
        """Print processing summary."""
        print("\n" + "="*60)
        print("🎯 LIVE DEBUG COMMUNICATION INGESTION SUMMARY")
        print("="*60)
        print(f"📁 Case ID: {self.case_id}")
        print(f"📂 Raw Directory: {self.raw_dir}")
        print(f"📄 Processed Directory: {self.processed_dir}")
        print(f"📞 Calls Processed: {'✅' if validation_results['calls_valid'] else '❌'}")
        print(f"💬 SMS Processed: {'✅' if validation_results['sms_valid'] else '❌'}")
        print(f"🔍 Pipeline Compatible: {'✅' if validation_results['schema_compatible'] else '❌'}")
        print("\n🔄 READY FOR FORENSIC PIPELINE:")
        print("   1. Timeline builder will merge CALL + SMS events")
        print("   2. Analysis scripts will process communication patterns")
        print("   3. UI will display calls and messages under live case")
        print("   4. Reports will include communication artifacts")
        print("="*60)
    
    def run(self):
        """Execute the complete live debug communication ingestion."""
        print("🚀 Starting Live Debug Communication Ingestion")
        print("=" * 60)
        
        # Print forensic transparency notice
        self.print_forensic_transparency_notice()
        
        # Ensure processed directory exists
        self.ensure_processed_directory()
        
        # Process communication logs
        calls_success = self.process_call_log()
        sms_success = self.process_sms_log()
        
        if not (calls_success and sms_success):
            print("❌ Communication processing failed")
            return False
        
        # Validate pipeline compatibility
        validation_results = self.validate_pipeline_compatibility()
        
        # Print summary
        self.print_summary(validation_results)
        
        return validation_results["schema_compatible"]

def main():
    """Main execution function."""
    print("Mobile Forensics - Live Debug Communication Ingestion Tool")
    print("=" * 70)
    print("🔒 DEBUG MODE: Processing simulated communication artifacts")
    print("   for pipeline validation and forensic workflow testing.")
    print("=" * 70)
    
    # Create and run ingestion tool
    ingestion = LiveDebugCommIngestion()
    success = ingestion.run()
    
    if success:
        print("\n🎉 Live debug communication ingestion completed successfully!")
        print("🔄 The forensic pipeline will now process the communication artifacts.")
    else:
        print("\n❌ Live debug ingestion failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
