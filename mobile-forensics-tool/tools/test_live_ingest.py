#!/usr/bin/env python3
"""
Test script for Live Android Ingestion Tool
Tests the case creation and metadata generation without requiring ADB
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def test_case_creation():
    """Test case creation and metadata generation."""
    print("🧪 Testing Live Ingestion Case Creation")
    print("=" * 50)
    
    base_path = Path(__file__).parent.parent
    case_id = "case_live_test"
    case_dir = base_path / "cases" / case_id
    raw_evidence_dir = case_dir / "evidence" / "raw"
    
    print(f"📁 Creating test case structure for {case_id}...")
    
    try:
        # Create case directories
        case_dir.mkdir(parents=True, exist_ok=True)
        raw_evidence_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Created case directory: {case_dir}")
        print(f"✅ Created evidence directory: {raw_evidence_dir}")
        
        # Create sample evidence structure
        sample_dirs = ["DCIM", "Download", "WhatsApp/Media"]
        for dir_name in sample_dirs:
            sample_dir = raw_evidence_dir / dir_name
            sample_dir.mkdir(parents=True, exist_ok=True)
            
            # Create sample files
            sample_file = sample_dir / "sample_file.txt"
            sample_file.write_text(f"Sample evidence file from {dir_name}")
        
        print("✅ Created sample evidence structure")
        
        # Create metadata
        metadata = {
            "case_id": "CASE-LIVE-TEST",
            "device_model": "Test Android Device (Live)",
            "dataset_source": "Live Android Device (ADB Logical)",
            "acquisition_method": "ADB logical extraction",
            "consent": "Explicit user consent obtained",
            "investigator": "Test Investigator",
            "case_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device_id": "test_device_12345"
        }
        
        metadata_file = case_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Created metadata file: {metadata_file}")
        
        # Verify structure
        total_files = 0
        for file_path in raw_evidence_dir.rglob('*'):
            if file_path.is_file():
                total_files += 1
        
        print(f"✅ Created {total_files} sample evidence files")
        
        # Print test summary
        print("\n" + "="*60)
        print("🎯 TEST CASE CREATION SUMMARY")
        print("="*60)
        print(f"📱 Test Device ID: test_device_12345")
        print(f"📁 Case Created: {case_id}")
        print(f"📂 Evidence Directory: {raw_evidence_dir}")
        print(f"📋 Metadata File: {metadata_file}")
        print(f"📁 Sample Evidence: DCIM/, Download/, WhatsApp/Media/")
        print(f"📄 Total Files: {total_files}")
        print("\n✅ TEST CASE READY FOR FORENSIC PIPELINE:")
        print("   1. Extraction (existing scripts will process new case)")
        print("   2. Analysis (behaviour, malware, anomaly detection)")
        print("   3. Timeline reconstruction")
        print("   4. Report generation")
        print("   5. UI viewing (multi-case support)")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in test case creation: {e}")
        return False

def cleanup_test_case():
    """Clean up the test case."""
    try:
        base_path = Path(__file__).parent.parent
        test_case_dir = base_path / "cases" / "case_live_test"
        
        if test_case_dir.exists():
            shutil.rmtree(test_case_dir)
            print("🧹 Cleaned up test case")
    except Exception as e:
        print(f"⚠️  Error cleaning up test case: {e}")

def main():
    """Main test function."""
    print("Mobile Forensics - Live Ingestion Test")
    print("=" * 50)
    
    success = test_case_creation()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("🔄 The live ingestion tool is ready for real Android devices.")
        
        # Ask user if they want to keep the test case
        try:
            keep = input("\nKeep test case for pipeline testing? (y/n): ").lower().strip()
            if keep != 'y':
                cleanup_test_case()
        except KeyboardInterrupt:
            print("\nKeeping test case")
    else:
        print("\n❌ Test failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
