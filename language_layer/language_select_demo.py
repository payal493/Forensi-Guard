from safety_generator import SafetySummaryGenerator

gen = SafetySummaryGenerator()

print("\n🔒 SAFETY ALERT GENERATOR\n")

# -------- Issue Type --------
print("Select Issue Type:")
print("1. location_tracking")
print("2. background_tracking")
print("3. stalkerware_indicators")

issue_choice = input()

issue_map = {
    "1": "location_tracking",
    "2": "background_tracking",
    "3": "stalkerware_indicators"
}

issue = issue_map.get(issue_choice, "location_tracking")

# -------- Risk Level --------
print("Select Risk Level:")
print("1. HIGH")
print("2. MEDIUM")
print("3. LOW")

risk_choice = input()

risk_map = {
    "1": "HIGH",
    "2": "MEDIUM",
    "3": "LOW"
}

risk = risk_map.get(risk_choice, "HIGH")

# -------- Language --------
print("Select Language:")
print("1. English")
print("2. Hindi")
print("3. Gujarati")

lang_choice = input()

lang_map = {
    "1": "english",
    "2": "hindi",
    "3": "gujarati"
}

language = lang_map.get(lang_choice, "english")

# -------- Generate Output --------
result = gen.generate_in_selected_language(risk, issue, language)

print("\n===========================")
print("Language:", result["language"].upper())
print("===========================\n")

print(result["message"])
print("\n", result["label"])
