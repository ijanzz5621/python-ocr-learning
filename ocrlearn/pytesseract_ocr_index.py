import pytesseract
from PIL import Image

def start():
    image_file = "data/index_02.JPG"
    img = Image.open(image_file)

    ocr_result = pytesseract.image_to_string(img)

    print(ocr_result)
    

