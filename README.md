[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OCR: EasyOCR](https://img.shields.io/badge/OCR-EasyOCR-orange.svg)](https://github.com/JaidedAI/EasyOCR)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](programa-para-traducir-imagenes-gsyke6cmwqcrjvmrappe8fr)

An advanced desktop solution for **automated text extraction, translation, and image inpainting**. Specifically optimized for visual storytelling media like comics and manga, this tool bridges the gap between raw foreign-language assets and localized digital content using AI-driven workflows.

---

## 🎯 Project Motivation & Strategic Vision

In today’s globalized digital economy, content localization is a critical strategic pillar. For media organizations, the manual translation of visual assets (manga, infographics, technical manuals) represents a massive operational bottleneck. 

This project aims to **digitalize the localization pipeline** by:
1.  **Reducing Operational Costs:** Automating the "clean-and-translate" cycle that usually requires multiple graphic designers and translators.
2.  **Accelerating Time-to-Market:** Enabling rapid prototyping of localized content.
3.  **Ensuring Data Consistency:** Maintaining a digital record of all translations for future training or auditing.

---

## 🖥️ Core Components & Interface

The application is built with a focus on user experience and technical precision through a robust **Tkinter-based GUI**:

*   **Dynamic Canvas Visualization:** Features a sophisticated coordinate scaling system. This ensures that user interactions on the screen correspond exactly to the original image pixels, regardless of window scaling.
*   **Centralized Control Hub:** Allows for seamless image importing, which triggers an automatic memory purge of previous translation history to prevent data conflicts.
*   **Real-time Status Logs:** A dedicated console provides live feedback (e.g., "Processing OCR...", "Translation Complete") to keep the user informed of background thread activities.

---

## ⚙️ Advanced Processing Modes

### A. Auto-Run (Automated Pipeline)
Designed for high-efficiency batch processing of full images.
*   **Paragraph Detection Logic:** Intelligent grouping of text lines based on proximity to maintain linguistic coherence.
*   **Contrast Filtering:** Analyzes color standard deviation to ignore non-textual areas (textures, speed lines, or background art) that often cause OCR hallucinations.
*   **Bulk Translation:** Automatically identifies speech bubbles, wipes the original text, and overlays the translation in a single pass.

### B. Manual Selection (Surgical Precision)
For complex layouts where AI might struggle.
*   **Bounding Box Interaction:** Users can drag-and-drop to define specific areas for processing.
*   **Interactive Editing Pop-up:** Upon selection, a dedicated window opens to allow:
    *   **OCR Correction:** Fix character misreadings (e.g., changing "I" to "l").
    *   **Translation Refining:** Manually adjust the AI's suggested translation before permanent embedding.
*   **Live Preview:** Confirm the placement and look of the text before committing to the original image.

---

## 🧠 Technical Logic & Image Pre-processing

To achieve high accuracy in Black & White media (Manga/Comics), the software employs a specialized **B/W Logic Module**:

| Technique | Description | Strategic Benefit |
| :--- | :--- | :--- |
| **Adaptive Otsu Thresholding** | Analyzes local lighting to separate text from background, even in shaded areas. | Increased OCR accuracy in low-contrast zones. |
| **Contour Filtering** | Filters out non-alphabetic shapes based on aspect ratio (e.g., ignoring long vertical lines). | Reduces noise and "garbage" text detection. |
| **Morphological Operations** | Applies Gaussian blur and dilation to "thicken" worn-out letters and erase digital dust. | Enhances readability for the AI engine. |

### Translation & Typography Engine
The `TranslatorLogic` module handles the bridge between image data and linguistic services:
*   **Multi-Engine Support:** Seamlessly integrates with Google Translate and DeepL via `deep-translator`.
*   **Punctuation Protection:** Specialized regex logic ensures that ellipses (...) and unique symbols are preserved during the translation round-trip.
*   **Dynamic Font Scaling:** Automatically calculates the optimal font size to ensure the translated text fits perfectly within the detected or selected bubble.
*   **Automatic Cleaning:** Automatically fixes common OCR errors, such as replacing sequences of underscores (`____`) with proper ellipses.
  
---

## linkedin
[My linkedin](https://www.linkedin.com/in/jose-luis-yuani-barea-17b745351)

---

## 🌐 Online Documentation
The professional technical documentation is available at:
[View Documentation Online](https://jyuanib.github.io/Programa-para-Traducir-imagenes/index.html)

---

## 💾 Data Management & Export

The system prioritizes **data integrity** through two main features:

1.  **Undo/Redo History Stack:** Before any change (manual or automatic) is applied, a pixel-perfect backup of the image is saved. This allows users to revert errors without losing previous progress.
2.  **Professional Export (Bilingual Format):**
    *   Generates a structured `.txt` file containing the full session history.
    *   Includes the original detected text alongside the final translation.
    *   **Symmetry:** If a user "undos" an action on the image, the corresponding entry is automatically removed from the export list to ensure the final report is accurate.

---

## 🛠️ Installation & Requirements

### System Dependencies
*   **Python 3.8+**
*   **EasyOCR Models:** Downloaded automatically on first run.
*   **PyTorch (torch):** For GPU acceleration (NVIDIA/CUDA recommended for professional workloads).

### Local Setup
```bash
# 1. Clone the repository
git clone https://github.com/jyuanib/Programa-para-Traducir-imagenes.git
cd Programa-para-Traducir-imagenes

# 2. Create a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install core libraries
pip install opencv-python pillow numpy easyocr deep-translator torch
