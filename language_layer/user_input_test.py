from safety_generator import SafetySummaryGenerator

gen = SafetySummaryGenerator()

english_msg = input("Enter safety message in English: ")

translated = gen.translate_custom_message(english_msg)

print("\nHindi:")
print(translated["hindi"])

print("\nGujarati:")
print(translated["gujarati"])
