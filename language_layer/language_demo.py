from safety_generator import SafetySummaryGenerator

gen = SafetySummaryGenerator()

print("\nChoose Language:")
print("1. English")
print("2. Hindi")
print("3. Gujarati")

choice = input("Enter choice: ")

lang_map = {"1": "english", "2": "hindi", "3": "gujarati"}
language = lang_map.get(choice, "english")

result = gen.generate_in_selected_language(
    "HIGH",
    "location_tracking",
    language
)

print("\nLanguage:", result["language"].upper())
print(result["message"])
