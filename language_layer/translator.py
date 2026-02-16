"""
Forensi-Guard Report Translator
Translates AI-generated report content to Hindi and Gujarati
while preserving forensic evidence integrity.

Features:
- Robust error handling with fallback to English
- Evidence integrity preservation (timestamps, numbers, hashes, etc.)
- Retry mechanism for failed translations
- Caching for performance
- UTF-8 encoding support
- Detailed logging

NOTE: Uses Google Translate API via googletrans library for demo.
For production, consider Google Cloud Translation API or LibreTranslate.
"""

import logging
import re
import time
from typing import Dict, Any, Optional
from functools import lru_cache

# Try to import googletrans for actual translation
try:
    from googletrans import Translator as GoogleTranslator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    print("⚠️  googletrans not available. Install with: pip install googletrans==4.0.0-rc1")

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ReportTranslator:
    """
    Translates AI report content to target languages with forensic integrity preservation.
    
    Features:
    - Preserves timestamps, numbers, coordinates, hashes, package names
    - Retry mechanism with exponential backoff
    - Caching for repeated translations
    - Graceful fallback to English on failure
    - UTF-8 encoding support
    - Detailed error logging
    """
    
    def __init__(self, use_real_translation: bool = True, max_retries: int = 3):
        """
        Initialize the translator.
        
        Args:
            use_real_translation: Use actual translation API if available
            max_retries: Maximum number of retry attempts for failed translations
        """
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'gu': 'Gujarati'
        }
        
        self.max_retries = max_retries
        self.use_real_translation = use_real_translation and GOOGLETRANS_AVAILABLE
        
        # Initialize Google Translator if available
        if self.use_real_translation:
            try:
                self.translator = GoogleTranslator()
                logger.info("ReportTranslator initialized with Google Translate")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Translator: {e}")
                self.use_real_translation = False
                logger.info("Falling back to mock translation")
        else:
            logger.info("ReportTranslator initialized in MOCK mode")
        
        # Patterns to protect from translation (forensic evidence)
        self.protected_patterns = [
            r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}',  # ISO timestamps
            r'\d{2}:\d{2}:\d{2}',  # Time
            r'\d{4}-\d{2}-\d{2}',  # Date
            r'\+?\d{10,15}',  # Phone numbers
            r'com\.[a-z0-9.]+',  # Package names
            r'[a-f0-9]{32,64}',  # Hashes
            r'-?\d+\.\d+',  # Coordinates/decimals
            r'[A-Z]{2,}_[A-Z_]+',  # Permission constants
            r'SHA-\d+',  # Hash algorithms
        ]
        
        # Compile regex patterns
        self.protected_regex = re.compile('|'.join(self.protected_patterns), re.IGNORECASE)
        
        # Translation cache
        self._cache = {}
        
        # Mock translations for fallback
        self.mock_translations = self._init_mock_translations()
    
    def _init_mock_translations(self) -> Dict[str, Dict[str, str]]:
        """Initialize mock translations for fallback."""
        return {
            'hi': {
                # Risk and threat terms
                'High-risk threat': 'उच्च जोखिम खतरा',
                'Medium-risk': 'मध्यम जोखिम',
                'Low-risk': 'कम जोखिम',
                'Critical': 'गंभीर',
                'Suspicious': 'संदिग्ध',
                'threat': 'खतरा',
                'risk': 'जोखिम',
                
                # Activity terms
                'location tracking': 'स्थान ट्रैकिंग',
                'activity detected': 'गतिविधि का पता चला',
                'privacy implications': 'गोपनीयता प्रभाव',
                'security concerns': 'सुरक्षा चिंताएं',
                
                # Analysis terms
                'Analysis of': 'विश्लेषण',
                'finding': 'खोज',
                'indicates': 'संकेत देता है',
                'significant': 'महत्वपूर्ण',
                'Multiple': 'कई',
                'indicators': 'संकेतक',
                'suggest': 'सुझाव देते हैं',
                'potential': 'संभावित',
                
                # App and permissions
                'The app': 'ऐप',
                'application': 'एप्लिकेशन',
                'has permission': 'अनुमति है',
                'to access': 'पहुंचने के लिए',
                'your': 'आपका',
                'precise GPS location': 'सटीक GPS स्थान',
                'allows': 'अनुमति देता है',
                'to track': 'ट्रैक करने के लिए',
                'exact coordinates': 'सटीक निर्देशांक',
                
                # Recommendations
                'Review': 'समीक्षा करें',
                'disable': 'अक्षम करें',
                'suspicious': 'संदिग्ध',
                'immediately': 'तुरंत',
                'Contact': 'संपर्क करें',
                'local': 'स्थानीय',
                'cyber harassment': 'साइबर उत्पीड़न',
                'support services': 'सहायता सेवाएं',
                'law enforcement': 'कानून प्रवर्तन',
                'Preserve': 'संरक्षित करें',
                'device evidence': 'डिवाइस साक्ष्य',
                'legal proceedings': 'कानूनी कार्यवाही',
                
                # Common phrases
                'detected': 'पता चला',
                'with': 'के साथ',
                'for': 'के लिए',
                'and': 'और',
                'or': 'या',
                'the': '',  # Often omitted in Hindi
            },
            'gu': {
                # Risk and threat terms
                'High-risk threat': 'ઉચ્ચ જોખમ ધમકી',
                'Medium-risk': 'મધ્યમ જોખમ',
                'Low-risk': 'ઓછું જોખમ',
                'Critical': 'ગંભીર',
                'Suspicious': 'શંકાસ્પદ',
                'threat': 'ધમકી',
                'risk': 'જોખમ',
                
                # Activity terms
                'location tracking': 'સ્થાન ટ્રેકિંગ',
                'activity detected': 'પ્રવૃત્તિ મળી',
                'privacy implications': 'ગોપનીયતા અસરો',
                'security concerns': 'સુરક્ષા ચિંતાઓ',
                
                # Analysis terms
                'Analysis of': 'વિશ્લેષણ',
                'finding': 'શોધ',
                'indicates': 'સૂચવે છે',
                'significant': 'નોંધપાત્ર',
                'Multiple': 'બહુવિધ',
                'indicators': 'સૂચકો',
                'suggest': 'સૂચવે છે',
                'potential': 'સંભવિત',
                
                # App and permissions
                'The app': 'એપ',
                'application': 'એપ્લિકેશન',
                'has permission': 'પરવાનગી છે',
                'to access': 'પહોંચવા માટે',
                'your': 'તમારા',
                'precise GPS location': 'ચોક્કસ GPS સ્થાન',
                'allows': 'મંજૂરી આપે છે',
                'to track': 'ટ્રેક કરવા માટે',
                'exact coordinates': 'ચોક્કસ કોઓર્ડિનેટ્સ',
                
                # Recommendations
                'Review': 'સમીક્ષા કરો',
                'disable': 'અક્ષમ કરો',
                'suspicious': 'શંકાસ્પદ',
                'immediately': 'તાત્કાલિક',
                'Contact': 'સંપર્ક કરો',
                'local': 'સ્થાનિક',
                'cyber harassment': 'સાયબર હેરાનગતિ',
                'support services': 'સહાય સેવાઓ',
                'law enforcement': 'કાયદા અમલીકરણ',
                'Preserve': 'સાચવો',
                'device evidence': 'ઉપકરણ પુરાવા',
                'legal proceedings': 'કાનૂની કાર્યવાહી',
                
                # Common phrases
                'detected': 'મળ્યું',
                'with': 'સાથે',
                'for': 'માટે',
                'and': 'અને',
                'or': 'અથવા',
                'the': '',  # Often omitted in Gujarati
            }
        }
    
    @lru_cache(maxsize=1000)
    def _translate_text_cached(self, text: str, target_lang: str) -> str:
        """
        Cached translation to avoid repeated API calls.
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            str: Translated text
        """
        return self._translate_text_internal(text, target_lang)
    
    def _translate_text_internal(self, text: str, target_lang: str) -> str:
        """
        Internal translation method with retry logic.
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            str: Translated text
        """
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return text
        
        # Use real translation if available
        if self.use_real_translation:
            for attempt in range(self.max_retries):
                try:
                    result = self.translator.translate(text, dest=target_lang, src='en')
                    if result and result.text:
                        logger.debug(f"Translated: '{text[:50]}...' -> '{result.text[:50]}...'")
                        return result.text
                except Exception as e:
                    logger.warning(f"Translation attempt {attempt + 1} failed: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(0.5 * (attempt + 1))  # Exponential backoff
                    else:
                        logger.error(f"All translation attempts failed for: {text[:50]}")
        
        # Fallback to mock translation
        return self._mock_translate(text, target_lang)
    
    def _mock_translate(self, text: str, target_lang: str) -> str:
        """
        Mock translation using predefined phrases.
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            str: Translated text or original if no translation available
        """
        if target_lang not in self.mock_translations:
            return text
        
        translations = self.mock_translations[target_lang]
        translated_text = text
        
        # Replace known phrases (case-insensitive)
        for english_phrase, translated_phrase in sorted(translations.items(), key=lambda x: -len(x[0])):
            if english_phrase.lower() in translated_text.lower():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(english_phrase), re.IGNORECASE)
                translated_text = pattern.sub(translated_phrase, translated_text)
        
        return translated_text
    
    def _protect_evidence(self, text: str) -> tuple:
        """
        Extract and protect forensic evidence from translation.
        
        Args:
            text: Text containing evidence
        
        Returns:
            tuple: (protected_text, evidence_map)
        """
        evidence_map = {}
        protected_text = text
        
        # Find all protected patterns
        matches = list(self.protected_regex.finditer(text))
        
        # Replace with placeholders
        for i, match in enumerate(matches):
            placeholder = f"__EVIDENCE_{i}__"
            evidence_map[placeholder] = match.group()
            protected_text = protected_text.replace(match.group(), placeholder, 1)
        
        return protected_text, evidence_map
    
    def _restore_evidence(self, text: str, evidence_map: Dict[str, str]) -> str:
        """
        Restore protected evidence after translation.
        
        Args:
            text: Translated text with placeholders
            evidence_map: Map of placeholders to original evidence
        
        Returns:
            str: Text with evidence restored
        """
        restored_text = text
        for placeholder, evidence in evidence_map.items():
            restored_text = restored_text.replace(placeholder, evidence)
        return restored_text
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """
        Translate text while preserving forensic evidence.
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            str: Translated text with evidence preserved
        """
        if not text or target_lang == 'en':
            return text
        
        try:
            # Protect evidence
            protected_text, evidence_map = self._protect_evidence(text)
            
            # Translate protected text
            translated_text = self._translate_text_cached(protected_text, target_lang)
            
            # Restore evidence
            final_text = self._restore_evidence(translated_text, evidence_map)
            
            return final_text
            
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return text  # Return original on error
    
    def translate_report(self, report: dict, target_language: str) -> dict:
        """
        Translate AI report to target language with forensic integrity preservation.
        
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
            start_time = time.time()
            logger.info(f"Starting translation to {target_language}")
            
            # Deep copy to avoid modifying original
            import copy
            translated_report = copy.deepcopy(report)
            
            # Translate each section
            if 'sections' in translated_report:
                sections = translated_report['sections']
                
                if 'executive_summary' in sections:
                    sections['executive_summary'] = self._translate_executive_summary(
                        sections['executive_summary'],
                        target_language
                    )
                
                if 'evidence_interpretation' in sections:
                    sections['evidence_interpretation'] = self._translate_evidence_interpretation(
                        sections['evidence_interpretation'],
                        target_language
                    )
                
                if 'timeline_narrative' in sections:
                    sections['timeline_narrative'] = self._translate_timeline_narrative(
                        sections['timeline_narrative'],
                        target_language
                    )
                
                if 'safety_recommendations' in sections:
                    sections['safety_recommendations'] = self._translate_safety_recommendations(
                        sections['safety_recommendations'],
                        target_language
                    )
            
            # Update language field
            translated_report['language'] = target_language
            
            elapsed_time = time.time() - start_time
            logger.info(f"Translation to {target_language} completed in {elapsed_time:.2f}s")
            
            return translated_report
            
        except Exception as e:
            logger.exception(f"Translation failed: {e}")
            logger.warning("Falling back to English")
            return report
    
    def _translate_executive_summary(self, exec_summary: dict, target_lang: str) -> dict:
        """Translate executive summary section."""
        import copy
        translated = copy.deepcopy(exec_summary)
        
        try:
            # Translate threat summary
            if 'threat_summary' in translated:
                translated['threat_summary'] = self.translate_text(
                    translated['threat_summary'],
                    target_lang
                )
            
            # Translate risk assessment reasoning
            if 'risk_assessment' in translated:
                risk = translated['risk_assessment']
                if 'reasoning' in risk:
                    risk['reasoning'] = self.translate_text(risk['reasoning'], target_lang)
                # Note: risk_level, risk_score, confidence are NOT translated (numbers/enums)
            
            # Translate key findings
            if 'key_findings' in translated:
                for finding in translated['key_findings']:
                    if 'finding' in finding:
                        finding['finding'] = self.translate_text(finding['finding'], target_lang)
                    # Note: confidence is NOT translated (number)
        
        except Exception as e:
            logger.error(f"Error translating executive summary: {e}")
        
        return translated
    
    def _translate_evidence_interpretation(self, evidence_interp: dict, target_lang: str) -> dict:
        """Translate evidence interpretation section (preserves technical data)."""
        import copy
        translated = copy.deepcopy(evidence_interp)
        
        try:
            # Translate artefact interpretations
            if 'artefacts' in translated:
                for artefact in translated['artefacts']:
                    if 'interpretation' in artefact:
                        artefact['interpretation'] = self.translate_text(
                            artefact['interpretation'],
                            target_lang
                        )
                    if 'reasoning' in artefact:
                        artefact['reasoning'] = self.translate_text(
                            artefact['reasoning'],
                            target_lang
                        )
                    # Note: 'original', 'type', 'timestamp' are NOT translated (evidence)
        
        except Exception as e:
            logger.error(f"Error translating evidence interpretation: {e}")
        
        return translated
    
    def _translate_timeline_narrative(self, timeline: dict, target_lang: str) -> dict:
        """Translate timeline narrative section."""
        import copy
        translated = copy.deepcopy(timeline)
        
        try:
            # Translate main narrative
            if 'narrative' in translated:
                translated['narrative'] = self.translate_text(
                    translated['narrative'],
                    target_lang
                )
            
            # Translate key events descriptions
            if 'key_events' in translated:
                for event in translated['key_events']:
                    if 'description' in event:
                        event['description'] = self.translate_text(
                            event['description'],
                            target_lang
                        )
                    # Note: 'timestamp' is NOT translated (evidence)
            
            # Translate patterns
            if 'patterns' in translated:
                translated['patterns'] = [
                    self.translate_text(pattern, target_lang)
                    for pattern in translated['patterns']
                ]
            
            # Note: event_count is NOT translated (number)
        
        except Exception as e:
            logger.error(f"Error translating timeline narrative: {e}")
        
        return translated
    
    def _translate_safety_recommendations(self, recommendations: dict, target_lang: str) -> dict:
        """Translate safety recommendations section."""
        import copy
        translated = copy.deepcopy(recommendations)
        
        try:
            # Translate recommendations
            if 'recommendations' in translated:
                for rec in translated['recommendations']:
                    if 'action' in rec:
                        rec['action'] = self.translate_text(rec['action'], target_lang)
                    if 'reasoning' in rec:
                        rec['reasoning'] = self.translate_text(rec['reasoning'], target_lang)
                    # Translate steps
                    if 'steps' in rec:
                        rec['steps'] = [
                            self.translate_text(step, target_lang)
                            for step in rec['steps']
                        ]
                    # Note: 'priority' is NOT translated (enum)
            
            # Translate disclaimer
            if 'disclaimer' in translated:
                translated['disclaimer'] = self.translate_text(
                    translated['disclaimer'],
                    target_lang
                )
        
        except Exception as e:
            logger.error(f"Error translating safety recommendations: {e}")
        
        return translated


# Convenience function for direct import
def translate_report(report: dict, target_language: str, use_real_translation: bool = True) -> dict:
    """
    Translate AI report to target language.
    
    Args:
        report: AI-generated report dictionary
        target_language: Target language code ('en', 'hi', or 'gu')
        use_real_translation: Use actual translation API if available
    
    Returns:
        dict: Translated report with forensic integrity preserved
        
    Example:
        >>> from language_layer.translator import translate_report
        >>> translated = translate_report(report, 'hi')
        >>> print(translated['language'])
        'hi'
    """
    translator = ReportTranslator(use_real_translation=use_real_translation)
    return translator.translate_report(report, target_language)

