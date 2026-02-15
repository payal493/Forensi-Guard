from safety_generator import SafetySummaryGenerator

gen = SafetySummaryGenerator()

issue_types = gen.get_supported_issue_types()

print("\n🔒 SAFETY ALERT GENERATOR\n")

# Show issue options
print("Select Issue Type:\n")
for i, issue in enumerate(issue_types, start=1):
    print(f"{i}. {issue}")

choice = int(input("\nEnter choice number: "))
selected_issue = issue_types[choice - 1]

print("\nSelect Risk Level:")
print("1. HIGH")
print("2. MEDIUM")
print("3. LOW")

risk_choice = input("Enter choice number: ")

risk_map = {
    "1": "HIGH",
    "2": "MEDIUM",
    "3": "LOW"
}

selected_risk = risk_map.get(risk_choice, "HIGH")

# Generate result
result = gen.generate_safety_summary(
    risk_level=selected_risk,
    issue_type=selected_issue,
    reasoning="demo",
    confidence=0.9
)

# Display result
print("\n==============================")
print(f"Issue: {selected_issue.upper()}")
print(f"Risk Level: {selected_risk}")
print("==============================")

print("\nENGLISH")
print(result["english"])

print("\nहिंदी")
print(result["hindi"])

print("\nગુજરાતી")
print(result["gujarati"])

print("\n⚠", result["label"])
