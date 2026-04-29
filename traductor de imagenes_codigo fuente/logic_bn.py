"""
Image processing module specialized in text/background separation for B/W media.
"""
import cv2
import numpy as np

class TextSeparator:
    """
    Provides computer vision filters to isolate text from complex backgrounds.
    """
    def __init__(self):
        self.filtro_activo = False

    def toggle(self):
        """
        Switches the active state of the B/W filter.

        Returns:
            bool: The new state of the filter.
        """
        self.filtro_activo = not self.filtro_activo
        return self.filtro_activo

    def validar_contraste(self, img_cv, bbox):
        """
        Checks if a Region of Interest (ROI) contains enough contrast to be text.

        Args:
            img_cv (numpy.ndarray): The source image in BGR format.
            bbox (list): Bounding box coordinates from OCR.

        Returns:
            bool: True if contrast is above threshold, False otherwise.
        """
        x1, y1, x2, y2 = int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])
        roi = img_cv[y1:y2, x1:x2]
        if roi.size == 0: return False
        gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        return np.std(gris) > 15 

    def aislar_texto(self, img_cv, bbox):
        """
        Applies Otsu thresholding and contour filtering to extract clean text.

        Args:
            img_cv (numpy.ndarray): The source image.
            bbox (list): Area to process.

        Returns:
            numpy.ndarray: A binary image (black text on white background) optimized for OCR.
        """
        x1, y1, x2, y2 = int(bbox[0][0]), int(bbox[0][1]), int(bbox[2][0]), int(bbox[2][1])
        roi = img_cv[y1:y2, x1:x2]
        
        gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(thresh)
        
        for c in contornos:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = w / float(h)
            if 0.1 < aspect_ratio < 4.0 and h > 5:
                cv2.drawContours(mask, [c], -1, 255, -1)
        
        return cv2.bitwise_not(mask)