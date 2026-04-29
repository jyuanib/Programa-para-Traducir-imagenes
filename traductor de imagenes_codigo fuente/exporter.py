"""
Module for exporting translated text data to external file formats.
"""
import os

class TextExporter:
    """
    Handles the serialization of translation data into human-readable text files.
    """
    @staticmethod
    def export_and_open(datos):
        """
        Generates a .txt file with bilingual results and opens it automatically.

        Args:
            datos (list): A list of dictionaries containing 'original' and 'traducido' keys.
        """
        filename = "texto_exportado.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== EXPORTED TEXT (WITH CHANGES) ===\n\n")
            for i, item in enumerate(datos, 1):
                f.write(f"[{i}] ORIGINAL: {item['original']}\n")
                f.write(f"    TRANSLATION: {item['traducido']}\n")
                f.write("-" * 40 + "\n")
        
        # Opens the file using the default system editor
        if os.name == 'nt':
            os.startfile(filename)