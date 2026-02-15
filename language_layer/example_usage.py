"""
Example usage of the Multilingual Safety Summary Generator
"""

from safety_generator import SafetySummaryGenerator
import json

def main():
    # Initialize the generator
    generator = SafetySummaryGenerator()
    
    # Example 1: Location tracking with HIGH risk
    print("=== Example 1: Location Tracking (HIGH Risk) ===")
    result1 = generator.generate_safety_summary(
        risk_level="HIGH",
        issue_type="location_tracking", 
        reasoning="App accesses precise location in background",
        confidence=0.87
    )
    print(json.dumps(result1, indent=2, ensure_ascii=False))
    print()
    
    # Example 2: Suspicious permissions with MEDIUM risk
    print("=== Example 2: Suspicious Permissions (MEDIUM Risk) ===")
    result2 = generator.generate_safety_summary(
        risk_level="MEDIUM",
        issue_type="suspicious_permissions",
        reasoning="App requests unnecessary camera and microphone access",
        confidence=0.65
    )
    print(json.dumps(result2, indent=2, ensure_ascii=False))
    print()
    
    # Example 3: Stalkerware indicators with HIGH risk
    print("=== Example 3: Stalkerware Indicators (HIGH Risk) ===")
    result3 = generator.generate_safety_summary(
        risk_level="HIGH",
        issue_type="stalkerware_indicators",
        reasoning="Hidden monitoring app detected with unusual permissions",
        confidence=0.92
    )
    print(json.dumps(result3, indent=2, ensure_ascii=False))
    print()
    
    # Example 4: Unknown issue type (uses default messages)
    print("=== Example 4: Unknown Issue Type (LOW Risk) ===")
    result4 = generator.generate_safety_summary(
        risk_level="LOW",
        issue_type="unknown_threat",
        reasoning="Unusual app behavior detected",
        confidence=0.45
    )
    print(json.dumps(result4, indent=2, ensure_ascii=False))
    print()
    
    # Example 5: Adding custom translation
    print("=== Example 5: Custom Translation ===")
    custom_translations = {
        'english': "Data usage is unusually high. This may indicate background activity.",
        'hindi': "डेटा उपयोग असामान्य रूप से अधिक है। यह बैकग्राउंड गतिविधि का संकेत हो सकता है।",
        'gujarati': "ડેટા વપરાશ અસામાન્ય રીતે વધારે છે. આ બેકગ્રાઉન્ડ પ્રવૃત્તિનો સંકેત હોઈ શકે છે."
    }
    
    generator.add_custom_translation('high_data_usage', 'medium', custom_translations)
    
    result5 = generator.generate_safety_summary(
        risk_level="MEDIUM",
        issue_type="high_data_usage",
        reasoning="App consuming excessive data in background",
        confidence=0.78
    )
    print(json.dumps(result5, indent=2, ensure_ascii=False))
    print()
    
    # Show supported issue types
    print("=== Supported Issue Types ===")
    print(generator.get_supported_issue_types())

if __name__ == "__main__":
    main()
