import numpy as np
import cv2


def removeBackground(image, mask):
    _, modified_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY_INV)

    Out_image = np.zeros_like(image)
    Out_image[modified_mask == 255] = image[modified_mask == 255]

    return Out_image


def removeClothBG(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, cloth_mask = cv2.threshold(img_gray, 5, 255, cv2.THRESH_BINARY)
    _, alpha = cv2.threshold(img_gray, 0, 1, cv2.THRESH_BINARY)

    # Extract out the image based on mask
    overlay = np.zeros_like(img)
    overlay[cloth_mask == 255] = img[cloth_mask == 255]

    # Add alpha channel for transparency
    if len(cv2.split(overlay)) == 4:
        b, g, r, a = cv2.split(overlay)
    else:
        b, g, r = cv2.split(overlay)

    RGBA_img = [b, g, r, alpha]
    BG_removed = cv2.merge(RGBA_img, 4)

    (y, x) = np.where(cloth_mask == 255)
    (top_y, top_x) = (np.min(y), np.min(x))
    (bottom_y, bottom_x) = (np.max(y), np.max(x))
    cropped_img = BG_removed[top_y:bottom_y + 1, top_x:bottom_x + 1]

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


def mergeImages(cloth_overlay, user_overlay):

    _, cloth_overlay_mask = cv2.threshold(cv2.cvtColor(cloth_overlay, cv2.COLOR_BGR2GRAY), 5, 255, cv2.THRESH_BINARY)
    user_overlay[cloth_overlay_mask == 255] = 0
    cv2.addWeighted(cloth_overlay, 1, user_overlay, 1, 0, user_overlay)

    return user_overlay