"""
Forensi-Guard Report Translator
Translates AI-generated report content to Hindi and Gujarati
while preserving forensic evidence integrity.

NOTE: This is a MOCK translator for demonstration purposes.
For production, integrate with actual translation API or service.
"""

import logging

logger = logging.getLogger(__name__)


class ReportTranslator:
    """
    Translates AI report content to target languages.
    
    CRITICAL: Only translates narrative text, findings, and recommendations.
    NEVER translates: timestamps, package names, numbers, coordinates, hashes.
    
    NOTE: This is a MOCK implementation for demo purposes.
    """
    
    def __init__(self):
        """Initialize the translator."""
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'gu': 'Gujarati'
        }
        
        # Mock translations for common phrases
        self.mock_translations = {
            'hi': {
                'High-risk threat': 'उच्च जोखिम खतरा',
                'Suspicious location tracking activity detected': 'संदिग्ध स्थान ट्रैकिंग गतिविधि का पता चला',
                'with privacy implications': 'गोपनीयता प्रभावों के साथ',
                'Analysis of': 'विश्लेषण',
                'finding(s) indicates significant risk': 'खोज महत्वपूर्ण जोखिम का संकेत देती है',
                'Multiple suspicious indicators suggest potential security concerns': 'कई संदिग्ध संकेतक संभावित सुरक्षा चिंताओं का सुझाव देते हैं',
                'The app': 'ऐप',
                'has permission to access your': 'आपके तक पहुंचने की अनुमति है',
                'precise GPS location': 'सटीक GPS स्थान',
                'This allows the app to track your exact coordinates': 'यह ऐप को आपके सटीक निर्देशांक ट्रैक करने की अनुमति देता है',
                'Review and disable suspicious applications immediately': 'संदिग्ध एप्लिकेशन की तुरंत समीक्षा करें और अक्षम करें',
                'Contact local cyber harassment support services or law enforcement': 'स्थानीय साइबर उत्पीड़न सहायता सेवाओं या कानून प्रवर्तन से संपर्क करें',
                'Preserve device evidence for potential legal proceedings': 'संभावित कानूनी कार्यवाही के लिए डिवाइस साक्ष्य संरक्षित करें'
            },
            'gu': {
                'High-risk threat': 'ઉચ્ચ જોખમ ધમકી',
                'Suspicious location tracking activity detected': 'શંકાસ્પદ સ્થાન ટ્રેકિંગ પ્રવૃત્તિ મળી',
                'with privacy implications': 'ગોપનીયતા અસરો સાથે',
                'Analysis of': 'વિશ્લેષણ',
                'finding(s) indicates significant risk': 'શોધ નોંધપાત્ર જોખમ સૂચવે છે',
                'Multiple suspicious indicators suggest potential security concerns': 'બહુવિધ શંકાસ્પદ સૂચકો સંભવિત સુરક્ષા ચિંતાઓ સૂચવે છે',
                'The app': 'એપ',
                'has permission to access your': 'તમારા સુધી પહોંચવાની પરવાનગી છે',
                'precise GPS location': 'ચોક્કસ GPS સ્થાન',
                'This allows the app to track your exact coordinates': 'આ એપને તમારા ચોક્કસ કોઓર્ડિનેટ્સ ટ્રેક કરવાની મંજૂરી આપે છે',
                'Review and disable suspicious applications immediately': 'શંકાસ્પદ એપ્લિકેશનોની તાત્કાલિક સમીક્ષા કરો અને અક્ષમ કરો',
                'Contact local cyber harassment support services or law enforcement': 'સ્થાનિક સાયબર હેરાનગતિ સહાય સેવાઓ અથવા કાયદા અમલીકરણનો સંપર્ક કરો',
                'Preserve device evidence for potential legal proceedings': 'સંભવિત કાનૂની કાર્યવાહી માટે ઉપકરણ પુરાવા સાચવો'
            }
        }
        
        logger.info("ReportTranslator initialized (MOCK mode)")
    
    def translate_report(self, report: dict, target_language: str) -> dict:
        """
        Translate AI report to target language.
        
        Args:
            report: AI-generated report dictionary
            target_language: Target language code ('hi' or 'gu')
        
        Returns:
            dict: Translated report with same structure
        """
        if target_language == 'en':
            return report  # No translation needed
        
        if target_language not in ['hi', 'gu']:
            logger.warning(f"Unsupported language: {target_language}, returning English")
            return report
        
        try:
            logger.info(f"Translating report to {target_language} (MOCK mode)")
            translated_report = report.copy()
            
            # Translate executive summary
            if 'sections' in translated_report and 'executive_summary' in translated_report['sections']:
                translated_report['sections']['executive_summary'] = self._translate_executive_summary(
                    translated_report['sections']['executive_summary'],
                    target_language
                )
            
            # Translate evidence interpretation
            if 'sections' in translated_report and 'evidence_interpretation' in translated_report['sections']:
                translated_report['sections']['evidence_interpretation'] = self._translate_evidence_interpretation(
                    translated_report['sections']['evidence_interpretation'],
                    target_language
                )
            
            # Translate timeline narrative
            if 'sections' in translated_report and 'timeline_narrative' in translated_report['sections']:
                translated_report['sections']['timeline_narrative'] = self._translate_timeline_narrative(
                    translated_report['sections']['timeline_narrative'],
                    target_language
                )
            
            # Translate safety recommendations
            if 'sections' in translated_report and 'safety_recommendations' in translated_report['sections']:
                translated_report['sections']['safety_recommendations'] = self._translate_safety_recommendations(
                    translated_report['sections']['safety_recommendations'],
                    target_language
                )
            
            # Update language field
            translated_report['language'] = target_language
            
            logger.info(f"Translation to {target_language} completed successfully")
            return translated_report
            
        except Exception as e:
            logger.exception(f"Translation failed: {e}")
            logger.warning("Falling back to English")
            return report
    
    def _translate_executive_summary(self, exec_summary: dict, target_lang: str) -> dict:
        """Translate executive summary section."""
        translated = exec_summary.copy()
        
        try:
            # Translate threat summary
            if 'threat_summary' in translated:
                translated['threat_summary'] = self._mock_translate(
                    translated['threat_summary'],
                    target_lang
                )
            
            # Translate risk assessment reasoning
            if 'risk_assessment' in translated and 'reasoning' in translated['risk_assessment']:
                translated['risk_assessment']['reasoning'] = self._mock_translate(
                    translated['risk_assessment']['reasoning'],
                    target_lang
                )
            
            # Translate key findings
            if 'key_findings' in translated:
                for finding in translated['key_findings']:
                    if 'finding' in finding:
                        finding['finding'] = self._mock_translate(
                            finding['finding'],
                            target_lang
                        )
        
        except Exception as e:
            logger.error(f"Error translating executive summary: {e}")
        
        return translated
    
    def _translate_evidence_interpretation(self, evidence_interp: dict, target_lang: str) -> dict:
        """Translate evidence interpretation section (preserves technical data)."""
        translated = evidence_interp.copy()
        
        try:
            # Translate artefact interpretations
            if 'artefacts' in translated:
                for artefact in translated['artefacts']:
                    if 'interpretation' in artefact:
                        artefact['interpretation'] = self._mock_translate(
                            artefact['interpretation'],
                            target_lang
                        )
                    if 'reasoning' in artefact:
                        artefact['reasoning'] = self._mock_translate(
                            artefact['reasoning'],
                            target_lang
                        )
        
        except Exception as e:
            logger.error(f"Error translating evidence interpretation: {e}")
        
        return translated
    
    def _translate_timeline_narrative(self, timeline: dict, target_lang: str) -> dict:
        """Translate timeline narrative section."""
        translated = timeline.copy()
        
        try:
            # Translate main narrative
            if 'narrative' in translated:
                translated['narrative'] = self._mock_translate(
                    translated['narrative'],
                    target_lang
                )
            
            # Translate key events descriptions
            if 'key_events' in translated:
                for event in translated['key_events']:
                    if 'description' in event:
                        event['description'] = self._mock_translate(
                            event['description'],
                            target_lang
                        )
            
            # Translate patterns
            if 'patterns' in translated:
                translated['patterns'] = [
                    self._mock_translate(pattern, target_lang)
                    for pattern in translated['patterns']
                ]
        
        except Exception as e:
            logger.error(f"Error translating timeline narrative: {e}")
        
        return translated
    
    def _translate_safety_recommendations(self, recommendations: dict, target_lang: str) -> dict:
        """Translate safety recommendations section."""
        translated = recommendations.copy()
        
        try:
            # Translate recommendations
            if 'recommendations' in translated:
                for rec in translated['recommendations']:
                    if 'action' in rec:
                        rec['action'] = self._mock_translate(rec['action'], target_lang)
                    if 'reasoning' in rec:
                        rec['reasoning'] = self._mock_translate(rec['reasoning'], target_lang)
                    # Translate steps
                    if 'steps' in rec:
                        rec['steps'] = [
                            self._mock_translate(step, target_lang)
                            for step in rec['steps']
                        ]
            
            # Translate disclaimer
            if 'disclaimer' in translated:
                translated['disclaimer'] = self._mock_translate(
                    translated['disclaimer'],
                    target_lang
                )
        
        except Exception as e:
            logger.error(f"Error translating safety recommendations: {e}")
        
        return translated
    
    def _mock_translate(self, text: str, target_lang: str) -> str:
        """
        Mock translation using predefined phrases.
        
        NOTE: This is a DEMO implementation. For production, use actual translation API.
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            str: Translated text or original if no translation available
        """
        if not text or not isinstance(text, str):
            return text
        
        if target_lang not in self.mock_translations:
            return text
        
        # Try to find matching phrases
        translations = self.mock_translations[target_lang]
        
        # Simple phrase replacement (for demo purposes)
        translated_text = text
        for english_phrase, translated_phrase in translations.items():
            if english_phrase.lower() in text.lower():
                translated_text = translated_text.replace(english_phrase, translated_phrase)
        
        # If no translation found, add language indicator
        if translated_text == text:
            if target_lang == 'hi':
                translated_text = f"[हिन्दी] {text}"
            elif target_lang == 'gu':
                translated_text = f"[ગુજરાતી] {text}"
        
        return translated_text


# Convenience function for direct import
def translate_report(report: dict, target_language: str) -> dict:
    """
    Translate AI report to target language.
    
    Args:
        report: AI-generated report dictionary
        target_language: Target language code ('en', 'hi', or 'gu')
    
    Returns:
        dict: Translated report
    """
    translator = ReportTranslator()
    return translator.translate_report(report, target_language)
