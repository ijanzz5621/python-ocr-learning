import pytesseract
#from PIL import Image
import cv2
import re

def start():
    
    image_file = cv2.imread("data/index_02.JPG")
    #ocr_result = pytesseract.image_to_string(image_file)
    #print(ocr_result)
    
    # PRE PROCESSING
    # ==============
    
    # 1. Convert to gray image
    gray = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)    
    # write 
    cv2.imwrite("temp/grayed_index_02.png", gray)

    # 2. Blur the image
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    # write
    cv2.imwrite("temp/blurred_index_02.png", blur)
    
    # 3. Create Threshold image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #print(thresh)
    cv2.imwrite("temp/thresh_index_02.png", thresh)
    
    # kernel & dailation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
    cv2.imwrite("temp/kernel_index_02.png", kernel)
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    cv2.imwrite("temp/dilate_index_02.png", dilate)
    
    # create contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key = lambda x: cv2.boundingRect(x)[0])
    
    cnt = 1
    result = []
    result_filtered = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h > 200 and w > 20:
            roi = image_file[y:y+h, x:x+w]
            cv2.imwrite(f"temp/roi_index_02_0{cnt}.png", roi)
            cv2.rectangle(image_file, (x, y), (x + w, y + h), (36, 255, 12), 2)
            ocr_result = pytesseract.image_to_string(roi)
            #print(ocr_result)
            ocr_result = ocr_result.split("\n")
            for item in ocr_result:
                #item = item.strip()
                #item = item.split(" ")[0]
                #print(item)            
                result.append(item)
                
            cnt = cnt + 1
    
    cv2.imwrite("temp/bbox_index_02.png", image_file)
    
    #print(result)
    for item in result:
        item = item.strip()
        item = item.split(" ")[0]
        #print(item)
        re_item = re.search(r"^[A-Z][a-z]+", item)
        if re_item is not None:
            result_filtered.append(re_item.group())
            #print(re_item.group())

    # make sure item in the list is unique by using the set()
    result_filtered = list(set(result_filtered))
    # sort the item in the list
    result_filtered.sort()
    print(result_filtered)