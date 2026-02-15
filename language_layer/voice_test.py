from safety_generator import SafetySummaryGenerator
from voice_alert import speak   # ✅ import speak function

gen = SafetySummaryGenerator()

result = gen.generate_safety_summary(
    risk_level="HIGH",
    issue_type="stalkerware_indicators",
    reasoning="Hidden monitoring detected",
    confidence=0.91
)

print("\n🔴 HIGH RISK DETECTED\n")

print("English:")
print(result["english"])

print("\nHindi:")
print(result["hindi"])

print("\nGujarati:")
print(result["gujarati"])

# 🔊 THIS LINE CALLS THE VOICE
print("\n🔊 Speaking alert...\n")
speak(result["hindi"])

input("\nPress ENTER to exit...")
