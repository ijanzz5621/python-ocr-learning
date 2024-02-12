import pytesseract
import cv2

def start():

    image = cv2.imread("data/sample_mgh.JPG")
    
    base_image = image.copy()

    #ocr_result = pytesseract.image_to_string(image)
    #print(ocr_result)
    
    # convert to grayscale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur it
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    # threshold it
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #print(thresh)
    
    # create the kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 50))
    # dilate it
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    
    cv2.imwrite("temp/mgh_dilate_result.png", dilate)
    
    # get the features using the contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #print(cnts)
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
    #print(cnts)
    
    # iterate the contours
    # create the bounding box for the dilate image
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h > 200 and w > 250:
            roi = base_image[y:y+h, x: x+w]
            cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
    
    # save the image with the boxes
    cv2.imwrite("temp/mgh_boxes_result.png", image)
    
    # test the pytesseract ocr with original and modified
    # note: modified will have more cleaner results
    ocr_result_original = pytesseract.image_to_string(base_image)
    ocr_result_modifed = pytesseract.image_to_string(image)    
    roi_result= pytesseract.image_to_string(roi)
    print(roi_result)
    
    
    
    