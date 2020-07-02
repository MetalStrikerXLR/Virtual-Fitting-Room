import cv2
import math as mt

from PyQt5.QtGui import QImage

import Kinect as Kv2
import ImageProcessing as IP
import numpy as np
import glob

shoulder_distance = 300
waist_distance = 300

SJR_x = 0
SJR_y = 0
SJL_x = 0
SJL_y = 0
Nk_x = 0
Nk_y = 0
HPL_x = 0
HPL_y = 0
HPR_x = 0
HPR_y = 0
SPB_x = 0
SPB_y = 0

# load cloth images
shirts = [cv2.imread(file, cv2.IMREAD_UNCHANGED) for file in glob.glob('Datasets/Shirts/*.png')]
pants = [cv2.imread(file, cv2.IMREAD_UNCHANGED) for file in glob.glob('Datasets/Pants/*.png')]
cropped_shirts = []
cropped_pants = []

# process and store cloth images
for items in shirts:
    shirt_processed = IP.removeClothBG(items)
    cropped_shirts.append(shirt_processed)

for items in pants:
    pant_processed = IP.removeClothBG(items)
    cropped_pants.append(pant_processed)

#############################
### Kinect runtime object ###
#############################

kinect = Kv2.initializeKinect()
color_width, color_height = Kv2.getColorDimension(kinect)

########################
### Main Kinect Loop ###
########################

while True:

    if kinect.has_new_body_frame() and kinect.has_new_color_frame():

        ##############################
        ### Get images from camera ###
        ##############################

        color_img, joint, jointpoints = Kv2.getKinectFrames(kinect, color_height, color_width)

        #################################################
        ### Extract and Draw 2D joints on single body ###
        #################################################

        if joint != 0:

            joint2D = Kv2.getBodyJoints(joint, jointpoints)
            SJR_x = int(joint2D[8, 0] * 3.75) + 30
            SJR_y = int(joint2D[8, 1] * 2.547) - 50
            SJL_x = int(joint2D[4, 0] * 3.75) + 30
            SJL_y = int(joint2D[4, 1] * 2.547) - 50
            Nk_x = int(joint2D[2, 0] * 3.75) + 30
            Nk_y = int(joint2D[2, 1] * 2.547) - 50
            HPL_x = int(joint2D[12, 0] * 3.75)
            HPL_y = int(joint2D[12, 1] * 2.547) - 50
            HPR_x = int(joint2D[16, 0] * 3.75) + 60
            HPR_y = int(joint2D[16, 1] * 2.547) - 50
            SPB_x = int(joint2D[0, 0] * 3.75) + 30
            SPB_y = int(joint2D[0, 1] * 2.547) - 50

            color_img = Kv2.drawJointsFull(color_img, joint2D)

            distance1 = mt.sqrt(mt.pow(SJL_x - SJR_x, 2))
            distance2 = mt.sqrt(mt.pow(HPL_x - HPR_x, 2))

        else:
            distance1 = 300
            distance2 = 300

        if distance1 <= 0:
            shoulder_distance = shoulder_distance
        else:
            shoulder_distance = distance1

        if distance2 <= 0:
            waist_distance = waist_distance
        else:
            waist_distance = distance2

        ##############################################
        ### Resizing Cloth image according to user ###
        ##############################################

        resized_shirt = IP.image_resize(cropped_shirts[1], width=int(shoulder_distance + 60))
        resized_pant = IP.image_resize(cropped_pants[3], width=int(waist_distance))

        shirt_y = np.shape(resized_shirt)[0]
        shirt_x = np.shape(resized_shirt)[1]
        pant_y = np.shape(resized_pant)[0]
        pant_x = np.shape(resized_pant)[1]

        #####################################################
        ### Add resized image to Background removed Image ###
        #####################################################

        # Offsets:
        overlay = np.zeros_like(color_img)
        overlay_y = np.shape(overlay)[0]
        overlay_x = np.shape(overlay)[1]

        # Pant addition
        cutoff_pants = (SPB_y + pant_y) - overlay_y
        if cutoff_pants <= 0:
            cutoff_pants = 0
        else:
            cutoff_pants = cutoff_pants

        if (HPL_x - 20) > 0 and SPB_y > 0 and (HPR_x + 70) < overlay_x:
            overlay[SPB_y:SPB_y + pant_y - cutoff_pants,
            int(SPB_x - (waist_distance / 2)):int(SPB_x - (waist_distance / 2)) + pant_x] = resized_pant[
                                                                                            0:pant_y - cutoff_pants,
                                                                                            0:pant_x]

        # Shirt addition
        if (SJL_x - 20) > 0 and Nk_y > 0 and (SJR_x + 70) < overlay_x:
            overlay[Nk_y:Nk_y + shirt_y, int(Nk_x - (shoulder_distance / 2) - 30):int(
                Nk_x - (shoulder_distance / 2) - 30) + shirt_x] = resized_shirt[0:shirt_y, 0:shirt_x]

        Output = IP.mergeImages(overlay, color_img)

        #####################################
        ## Display 2D images using OpenCV ###
        #####################################

        cv2.imshow('Virtual Fitting Room', color_img)

    key = cv2.waitKey(30)
    if key == 27:  # Press esc to break the loop
        break

kinect.close()
cv2.destroyAllWindows()
