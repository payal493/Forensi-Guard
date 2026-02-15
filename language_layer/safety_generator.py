"""
Multilingual Safety Summary Generator for Forensi-Guard
Provides multilingual safety explanations with user-selected language output.
"""

class SafetySummaryGenerator:
    def __init__(self):

        # -------------------------------
        # SAFETY MESSAGES
        # -------------------------------
        self.translations = {

            'location_tracking': {
                'english': {
                    'high': "Your location is being tracked frequently. This could put your safety at risk.",
                    'medium': "Some apps may be accessing your location.",
                    'low': "Location access is enabled on your device."
                },
                'hindi': {
                    'high': "आपका स्थान लगातार ट्रैक किया जा रहा है। यह आपकी सुरक्षा के लिए खतरा हो सकता है।",
                    'medium': "कुछ ऐप्स आपके स्थान तक पहुंच सकते हैं।",
                    'low': "आपके डिवाइस पर स्थान पहुंच सक्षम है।"
                },
                'gujarati': {
                    'high': "તમારું સ્થાન વારંવાર ટ્રેક થઈ રહ્યું છે. આ તમારી સુરક્ષા માટે જોખમી હોઈ શકે છે.",
                    'medium': "કેટલીક એપ્સ તમારા સ્થાનને ઍક્સેસ કરી શકે છે.",
                    'low': "તમારા ઉપકરણમાં સ્થાન ઍક્સેસ સક્રિય છે."
                }
            },

            'background_tracking': {
                'english': {
                    'high': "Apps are monitoring your activity in the background.",
                    'medium': "Some apps may track background activity.",
                    'low': "Background activity detected."
                },
                'hindi': {
                    'high': "ऐप्स बैकग्राउंड में आपकी गतिविधि की निगरानी कर रहे हैं।",
                    'medium': "कुछ ऐप्स बैकग्राउंड गतिविधि ट्रैक कर सकते हैं।",
                    'low': "बैकग्राउंड गतिविधि का पता चला।"
                },
                'gujarati': {
                    'high': "એપ્સ બેકગ્રાઉન્ડમાં તમારી પ્રવૃત્તિનું નિરીક્ષણ કરી રહી છે.",
                    'medium': "કેટલીક એપ્સ બેકગ્રાઉન્ડ પ્રવૃત્તિ ટ્રેક કરી શકે છે.",
                    'low': "બેકગ્રાઉન્ડ પ્રવૃત્તિ મળી."
                }
            },

            'stalkerware_indicators': {
                'english': {
                    'high': "Monitoring software indicators detected. Your device may be compromised.",
                    'medium': "Possible monitoring software found.",
                    'low': "Unusual app behaviour detected."
                },
                'hindi': {
                    'high': "मॉनिटरिंग सॉफ्टवेयर के संकेत मिले। आपका डिवाइस समझौता किया जा सकता है।",
                    'medium': "संभावित मॉनिटरिंग सॉफ्टवेयर मिला।",
                    'low': "असामान्य ऐप व्यवहार का पता चला।"
                },
                'gujarati': {
                    'high': "મોનિટરિંગ સોફ્ટવેરના સંકેતો મળ્યા. તમારું ઉપકરણ સંક્રમિત થઈ શકે છે.",
                    'medium': "સંભવિત મોનિટરિંગ સોફ્ટવેર મળ્યું.",
                    'low': "અસામાન્ય એપ વર્તન મળ્યું."
                }
            }
        }

        # fallback messages
        self.default_messages = {
            "english": "Security risk detected. Please review device settings.",
            "hindi": "सुरक्षा जोखिम का पता चला। कृपया डिवाइस सेटिंग्स जांचें।",
            "gujarati": "સુરક્ષા જોખમ મળ્યું. કૃપા કરીને ઉપકરણ સેટિંગ્સ તપાસો."
        }

    # ------------------------------------------------
    # MULTILINGUAL GENERATOR (ALL LANGUAGES)
    # ------------------------------------------------
    def generate_safety_summary(self, risk_level, issue_type):
        risk_level = risk_level.lower()
        issue_type = issue_type.lower()

        english = self._get_message(issue_type, risk_level, "english")
        hindi = self._get_message(issue_type, risk_level, "hindi")
        gujarati = self._get_message(issue_type, risk_level, "gujarati")

        # Add safety advice for HIGH risk
        if risk_level == "high":
            english += "\nIf you feel unsafe, report at cybercrime.gov.in"
            hindi += "\nयदि आप असुरक्षित महसूस करते हैं, cybercrime.gov.in पर शिकायत करें।"
            gujarati += "\nજો તમને અસુરક્ષિત લાગે, cybercrime.gov.in પર ફરિયાદ કરો."

        return {
            "english": english,
            "hindi": hindi,
            "gujarati": gujarati,
            "label": "⚠ AI-Generated Safety Insight"
        }

    # ------------------------------------------------
    # USER-SELECTED LANGUAGE OUTPUT
    # ------------------------------------------------
    def generate_in_selected_language(self, risk_level, issue_type, language):
        """
        Return safety message in the user-selected language.
        """

        language = language.lower()

        result = self.generate_safety_summary(risk_level, issue_type)

        if language not in ["english", "hindi", "gujarati"]:
            return {
                "message": "Invalid language selection.",
                "label": result["label"]
            }

        return {
            "language": language,
            "message": result[language],
            "label": result["label"]
        }

    # ------------------------------------------------
    # INTERNAL MESSAGE FETCHER
    # ------------------------------------------------
    def _get_message(self, issue, level, lang):
        if issue in self.translations:
            return self.translations[issue][lang].get(level,
                                                      self.default_messages[lang])
        return self.default_messages[lang]
