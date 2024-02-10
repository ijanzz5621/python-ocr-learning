import cv2
import matplotlib.pyplot as plt

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    height, width, depth = im_data.shape
    print(f"height = {height}")
    print(f"width = {width}")
    print(f"depth = {depth}")
    
    figsize = width / float(dpi), height / float(dpi)
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    ax.imshow(im_data, cmap='plasma')
    plt.show()

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    import numpy as np
    
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1,1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)    
    # morph
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    
    return image

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def start():
    image_file = "data/page_01.jpg"

    img = cv2.imread(image_file)

    #cv2.imshow("original image", img)
    #cv2.waitKey(0)
    #display(image_file)
    
    # 1. Invert image
    inverted_image = cv2.bitwise_not(img)
    # Save
    cv2.imwrite("temp/inverted_page_01.jpg", inverted_image)
    # Display
    #display("temp/inverted_page_01.jpg")
    
    # # 2. Binarization
    gray_image = grayscale(img)
    cv2.imwrite("temp/grayed_page_01.jpg", gray_image)
    #display("temp/grayed_page_01.jpg",)
    
    # Binarize it
    thres, im_bw = cv2.threshold(gray_image, 200, 230, cv2.THRESH_BINARY)
    cv2.imwrite("temp/blackwhite_page_01.jpg", im_bw)
    #display("temp/blackwhite_page_01.jpg")
    
    # 3. Noise Removal
    noise_remove_image = noise_removal(im_bw)
    cv2.imwrite("temp/noiseremoved_page_01.jpg", noise_remove_image)
    #display("temp/noiseremoved_page_01.jpg")
    
    # 4. Dilation & Erosion
    eroded_image = thin_font(noise_remove_image)
    cv2.imwrite("temp/eroded_page_01.jpg", eroded_image)
    dilated_image = thick_font(noise_remove_image)
    cv2.imwrite("temp/dilated_page_01.jpg", dilated_image)
    
    # 5. Rotation / Deskewing
    skew_image = cv2.imread("data/page_01_rotated.JPG")
    cv2.imwrite("temp/original_rotated_page_01.JPG", skew_image)
    #display("data/page_01_rotated.JPG")    
    angle = getSkewAngle(skew_image)    
    deskew_image = rotateImage(skew_image, -angle)
    cv2.imwrite("temp/deskew_page_01.JPG", deskew_image)
    
    