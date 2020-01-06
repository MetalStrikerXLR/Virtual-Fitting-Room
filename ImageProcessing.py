import numpy as np
import cv2


def removeBackground(image, mask):
    _, modified_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)

    Out_image = np.zeros_like(image)
    Out_image[modified_mask == 255] = image[modified_mask == 255]

    return Out_image


def removeClothBK(grayscale_img, orig_img):
    _, cloth_mask = cv2.threshold(grayscale_img, 127, 255, 0)
    # contours, _ = cv2.findContours(cloth_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(cloth_mask, contours, 16, 255, -1)

    Bkremoved = np.zeros_like(orig_img)  # Extract out the object and place into output image
    Bkremoved[cloth_mask == 255] = orig_img[cloth_mask == 255]

    (y, x) = np.where(cloth_mask == 255)
    (top_y, top_x) = (np.min(y), np.min(x))
    (bottom_y, bottom_x) = (np.max(y), np.max(x))
    cropped_img = Bkremoved[top_y:bottom_y + 1, top_x:bottom_x + 1]

    return cropped_img


def resizeCloths(distance, image):
    scale_percent = (distance / image.shape[1]) * 100  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized