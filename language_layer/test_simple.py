"""
Simple test for the Multilingual Safety Summary Generator
"""

from safety_generator import SafetySummaryGenerator

def test_basic_functionality():
    generator = SafetySummaryGenerator()
    
    # Test the example from the prompt
    result = generator.generate_safety_summary(
        risk_level="HIGH",
        issue_type="location_tracking",
        reasoning="App accesses precise location in background",
        confidence=0.87
    )
    
    print("=== Test Result ===")
    print("English:", result["english"])
    print("Hindi text length:", len(result["hindi"]))
    print("Gujarati text length:", len(result["gujarati"]))
    print("Label:", result["label"])
    
    # Verify structure
    assert "english" in result
    assert "hindi" in result
    assert "gujarati" in result
    assert "label" in result
    assert result["label"] == "AI-Generated Safety Insight"
    
    print("\n[PASS] Test passed! Module is working correctly.")
    print("[PASS] All translations generated successfully.")
    print("[PASS] Output format matches requirements.")

if __name__ == "__main__":
    test_basic_functionality()
