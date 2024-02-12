import ocrlearn.ocr_test1 as ocr_test1
import ocrlearn.ocr_oepncv as ocr_opencv
import ocrlearn.pytesseract_example as pytesseract_example
import ocrlearn.pytesseract_ocr_index as ocr_index
import ocrlearn.pytesseract_bounding_box as ocr_box
import ocrlearn.ocr_marginalia as ocr_mgh
import ocrlearn.ocr_marginalia_seperate_footnote as ocr_mgh_sep_ft

def main() -> None:
    print("Welcome to OCR learning platform.")
    #ocr_test1.start_ocr()
    #ocr_opencv.start()
    #pytesseract_example.start()
    #ocr_index.start()
    #ocr_box.start()
    #ocr_mgh.start()
    ocr_mgh_sep_ft.start()

if __name__ == "__main__":
    main()