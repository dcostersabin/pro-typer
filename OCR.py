import cv2
import pytesseract
from abc import ABC


class ImageToChar(ABC):

    def __init__(self):
        self.image = None
        self.contours = None
        self.prediction = None
        super().__init__()

    def __preprocess(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        ret, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        dialation = cv2.dilate(threshold, rect_kernel, iterations=1)

        self.contours, hierarchy = cv2.findContours(dialation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    def __generate_predictions(self):
        for cnt in self.contours:
            x, y, w, h = cv2.boundingRect(cnt)

            cropped = self.image[y:y + h, x:x + w]

            self.prediction = pytesseract.image_to_string(cropped)

    def predict(self):
        self.__preprocess()
        self.__generate_predictions()


