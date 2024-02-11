import pytesseract
from PIL import Image

def start():
    img_file = "data/page_01.jpg"
    no_noise_img_file = "temp/noiseremoved_page_01.jpg"

    #img = Image.open(img_file)
    img = Image.open(no_noise_img_file)

    ocr_result = pytesseract.image_to_string(img)

    print("OCR result as below:")

    print(ocr_result)
