from voice_input import listen

translation_map = {
    "hello": {
        "hindi": "नमस्ते",
        "gujarati": "નમસ્તે"
    },
    "bhojpuri": {
        "hindi": "भोजपुरी",
        "gujarati": "ભોજપુરી"
    },
    "test": {
        "hindi": "परीक्षण",
        "gujarati": "પરીક્ષણ"
    }
}

spoken_text = listen()

if spoken_text:
    word = spoken_text.lower()

    print("\nHindi:")
    print(translation_map.get(word, "अनुवाद उपलब्ध नहीं"))

    print("\nGujarati:")
    print(translation_map.get(word, "અનુવાદ ઉપલબ્ધ નથી"))
