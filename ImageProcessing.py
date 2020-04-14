import numpy as np
import cv2


def removeBackground(image, mask):
    _, modified_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)

    Out_image = np.zeros_like(image)
    Out_image[modified_mask == 255] = image[modified_mask == 255]

    return Out_image


def removeClothBK(grayscale_img, orig_img):
    _, cloth_mask = cv2.threshold(grayscale_img, 127, 255, 0)
    _, alpha = cv2.threshold(grayscale_img, 0, 255, cv2.THRESH_BINARY)
    #contours, _ = cv2.findContours(cloth_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(orig_img, contours, -1, (1, 255, 0), 2)

    overlay = np.zeros_like(orig_img)  # Extract out the object and place into output image
    overlay[cloth_mask == 255] = orig_img[cloth_mask == 255]
    b, g, r, a = cv2.split(overlay)
    rgba = [b, g, r, alpha]
    Bkremoved = cv2.merge(rgba, 4)

    (y, x) = np.where(cloth_mask == 255)
    (top_y, top_x) = (np.min(y), np.min(x))
    (bottom_y, bottom_x) = (np.max(y), np.max(x))
    cropped_img = Bkremoved[top_y:bottom_y + 1, top_x:bottom_x + 1]

    return cropped_img


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized