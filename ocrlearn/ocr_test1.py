import cv2
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

def start_ocr():
    print("OCR Started!") 
    
    im_file = "data/page_01.jpg"
    
    im = Image.open(im_file)
    
    print(im)
    
    #im.show()
    im.rotate(180).show()
    
    im.save("temp/page_01.jpg")
    
    