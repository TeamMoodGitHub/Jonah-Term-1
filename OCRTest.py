import os
import pytesseract
from PIL import Image



pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
TESSDATA_PREFIX='C:\Program Files (x86)\Tesseract-OCR'
print pytesseract.image_to_string(Image.open('F:\\Work\\CvTest\\percents.png')).encode("utf-8")