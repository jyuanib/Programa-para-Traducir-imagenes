"""
Core translation and drawing logic using EasyOCR and Deep-Translator.
"""
import re
import easyocr
from deep_translator import GoogleTranslator
from PIL import ImageFont, ImageDraw

# Initialize EasyOCR Reader with GPU support
reader = easyocr.Reader(['en', 'es'], gpu=True)

class TranslatorLogic:
    """
    Handles linguistic transformations and visual embedding of text.
    """
    @staticmethod
    def translate_text(text):
        """
        Cleans OCR noise and translates text while preserving symbols.

        Args:
            text (str): The raw text extracted by OCR.

        Returns:
            str: The translated text in Spanish.
        """
        if not text or not text.strip(): return ""
        # Regex cleaning for common OCR artifacts
        text = re.sub(r'_{2,}', '...', text)
        
        try:
            traduccion = GoogleTranslator(source='auto', target='es').translate(text)
            return traduccion
        except:
            return text

    @staticmethod
    def draw_text_on_image(img_pil, text, box):
        """
        Inpaints the original area and draws the new text with dynamic scaling.

        Args:
            img_pil (PIL.Image): The main workspace image.
            text (str): Translated string to draw.
            box (tuple): (x1, y1, x2, y2) coordinates.
        """
        draw = ImageDraw.Draw(img_pil)
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], fill="white")
        
        w_box, h_box = x2 - x1, y2 - y1
        f_size = int(h_box * 0.85)
        
        # Iteratively find the best font size to fit the box
        while f_size > 6:
            try: font = ImageFont.truetype("arial.ttf", f_size)
            except: font = ImageFont.load_default()
            
            # Text wrapping logic...
            # (Rest of your drawing implementation)
            break