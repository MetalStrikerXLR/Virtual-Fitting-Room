import cv2
import math as mt
import Kinect as Kv2
import ImageProcessing as IP
import numpy as np
import time
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
HTL_x = 0
HTL_y = 0
HTR_x = 0
HTR_y = 0

icon1_state = 0
icon2_state = 0
icon3_state = 0
icon4_state = 0

# load icons
icons = [cv2.imread(file, cv2.IMREAD_UNCHANGED) for file in glob.glob('icons/*.png')]
cropped_icons = []

# process and store icon images
for items in icons:
    icon_processed = IP.processIcons(items, 30)
    cropped_icons.append(icon_processed)

# load cloth images
shirts = [cv2.imread(file, cv2.IMREAD_UNCHANGED) for file in glob.glob('Datasets/Shirts/*.png')]
pants = [cv2.imread(file, cv2.IMREAD_UNCHANGED) for file in glob.glob('Datasets/Pants/*.png')]
cropped_shirts = []
cropped_pants = []

# process and store cloth images
for items in shirts:
    shirt_processed = IP.removeClothBG(items)
    cropped_shirts.append(shirt_processed)

current_shirt = cropped_shirts[0]
si = 0

for items in pants:
    pant_processed = IP.removeClothBG(items)
    cropped_pants.append(pant_processed)

current_pant = cropped_pants[0]
pi = 0

total_shirts = len(cropped_shirts)
total_pants = len(cropped_pants)

#########################
### Store timer state ###
#########################

previous_time = time.time()

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

        color_img, joint, jointpoints = Kv2.getKinectFrames(kinect, color_height, color_width, True)

        #################################################
        ### Extract and Draw 2D joints on single body ###
        #################################################

        if joint != 0:

            joint2D = Kv2.getBodyJoints(joint, jointpoints)
            SJR_x = joint2D[8, 0]
            SJR_y = joint2D[8, 1]
            SJL_x = joint2D[4, 0]
            SJL_y = joint2D[4, 1]
            Nk_x = joint2D[2, 0]
            Nk_y = joint2D[2, 1]
            HPL_x = joint2D[12, 0]
            HPL_y = joint2D[12, 1]
            HPR_x = joint2D[16, 0]
            HPR_y = joint2D[16, 1]
            SPB_x = joint2D[0, 0]
            SPB_y = joint2D[0, 1]
            HTL_x = joint2D[7, 0]
            HTL_y = joint2D[7, 1]
            HTR_x = joint2D[11, 0]
            HTR_y = joint2D[11, 1]

            # color_img = Kv2.drawJoints(color_img, joint2D)
            cv2.circle(color_img, (HTL_x, HTL_y), 20, (66, 212, 245), -1)
            cv2.circle(color_img, (HTR_x, HTR_y), 20, (66, 212, 245), -1)

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

        ##############################################################
        ### Detect button state from GUI and set cloth accordingly ###
        ##############################################################

        if icon4_state == 1:
            if icon1_state == 1:
                current_time = time.time()
                duration = current_time - previous_time

                if duration >= 1:
                    si = (si - 1) % total_shirts
                    current_shirt = cropped_shirts[si]
                    previous_time = time.time()

            if icon2_state == 1:
                current_time = time.time()
                duration = current_time - previous_time

                if duration >= 1:
                    si = (si + 1) % total_shirts
                    current_shirt = cropped_shirts[si]
                    previous_time = time.time()

        if icon3_state == 1:
            if icon1_state == 1:
                current_time = time.time()
                duration = current_time - previous_time

                if duration >= 1:
                    pi = (pi - 1) % total_pants
                    current_pant = cropped_pants[pi]
                    previous_time = time.time()

            if icon2_state == 1:
                current_time = time.time()
                duration = current_time - previous_time

                if duration >= 1:
                    pi = (pi + 1) % total_pants
                    current_pant = cropped_pants[pi]
                    previous_time = time.time()

        ##############################################
        ### Resizing Cloth image according to user ###
        ##############################################

        resized_shirt = IP.image_resize(current_shirt, width=int(shoulder_distance + 120))
        resized_pant = IP.image_resize(current_pant, width=int(waist_distance + 110))

        shirt_y = np.shape(resized_shirt)[0]
        shirt_x = np.shape(resized_shirt)[1]
        pant_y = np.shape(resized_pant)[0]
        pant_x = np.shape(resized_pant)[1]

        #####################################################
        ### Add resized image to User Image ###
        #####################################################

        # Offsets:
        overlay_pants = np.zeros_like(color_img)
        overlay_shirts = np.zeros_like(color_img)
        overlay_y = np.shape(overlay_pants)[0]
        overlay_x = np.shape(overlay_pants)[1]

        # Pant addition
        cutoff_pants = (SPB_y + pant_y) - overlay_y
        if cutoff_pants <= 0:
            cutoff_pants = 0
        else:
            cutoff_pants = cutoff_pants

        if 0 < pant_y < overlay_y and 0 < pant_x < overlay_x and 0 < SPB_y < overlay_y and 0 < SPB_x - 55 < overlay_x:
            overlay_pants[SPB_y:SPB_y + pant_y - cutoff_pants,
            int(SPB_x - (waist_distance / 2) - 55):int(SPB_x - (waist_distance / 2)) + pant_x - 55] = resized_pant[
                                                                                            0:pant_y - cutoff_pants,
                                                                                            0:pant_x]

        # Shirt addition
        # cutoff_shirts = (Nk_y - 10 + shirt_y) - overlay_y
        # if cutoff_shirts <= 0:
        #     cutoff_shirts = 0
        # else:
        #     cutoff_shirts = cutoff_shirts

        if 0 < shirt_y < overlay_y and 0 < shirt_x < overlay_x and 0 < Nk_y - 10 < overlay_y and 0 < Nk_x - 60 < overlay_x:
            overlay_shirts[Nk_y - 10:Nk_y + shirt_y - 10, int(Nk_x - (shoulder_distance / 2) - 60):int(
                Nk_x - (shoulder_distance / 2) - 60) + shirt_x] = resized_shirt[0:shirt_y, 0:shirt_x]
        layer1 = IP.mergeImages(overlay_shirts, overlay_pants)
        layer2 = IP.mergeImages(layer1, color_img)

        ##################################
        ## Add GUI functions and Icons ###
        ##################################

        icon_y = np.shape(cropped_icons[0])[0]
        icon_x = np.shape(cropped_icons[0])[1]

        icon_overlay = np.zeros_like(layer2)
        icon_overlay_y = np.shape(icon_overlay)[0]
        icon_overlay_x = np.shape(icon_overlay)[1]

        # check buttons
        if (530 < HTL_x < icon_x + 530) and (
                int((icon_overlay_y / 2) - (icon_y / 2)) < HTL_y < int((icon_overlay_y / 2) - (icon_y / 2)) + icon_y):
            icon1_state = 1
        else:
            icon1_state = 0

        if (int(icon_overlay_x - icon_x) - 530 < HTR_x < icon_overlay_x - 530) and (
                int((icon_overlay_y / 2) - (icon_y / 2)) < HTR_y < int(
                (icon_overlay_y / 2) - (icon_y / 2)) + icon_y):
            icon2_state = 1
        else:
            icon2_state = 0

        if (int(icon_overlay_x / 2 - 2 * icon_x) < HTL_x < int(icon_overlay_x / 2 - icon_x)) and (
                25 < HTL_y < icon_y + 25):
            icon3_state = 1
            icon4_state = 0

        if (int(icon_overlay_x / 2 + icon_x) < HTR_x < int(icon_overlay_x / 2 + 2 * icon_x)) and (
                25 < HTR_y < icon_y + 25):
            icon4_state = 1
            icon3_state = 0

        # generate icon overlay
        if icon1_state == 1:
            icon1 = cropped_icons[6]
        else:
            icon1 = cropped_icons[0]

        if icon2_state == 1:
            icon2 = cropped_icons[7]
        else:
            icon2 = cropped_icons[1]

        if icon3_state == 1:
            icon3 = cropped_icons[3]
        else:
            icon3 = cropped_icons[2]

        if icon4_state == 1:
            icon4 = cropped_icons[5]
        else:
            icon4 = cropped_icons[4]

        icon_overlay[int((icon_overlay_y / 2) - (icon_y / 2)):int((icon_overlay_y / 2) - (icon_y / 2)) + icon_y,
        530:icon_x + 530] = icon1[0:icon_y, 0:icon_x]
        icon_overlay[int((icon_overlay_y / 2) - (icon_y / 2)):int((icon_overlay_y / 2) - (icon_y / 2)) + icon_y,
        int(icon_overlay_x - icon_x) - 530:icon_overlay_x - 530] = icon2[0:icon_y, 0:icon_x]
        icon_overlay[25:icon_y + 25, int(icon_overlay_x / 2 - 2 * icon_x):int(icon_overlay_x / 2 - icon_x)] = icon3[
                                                                                                              0:icon_y,
                                                                                                              0:icon_x]
        icon_overlay[25:icon_y + 25, int(icon_overlay_x / 2 + icon_x):int(icon_overlay_x / 2 + 2 * icon_x)] = icon4[
                                                                                                              0:icon_y,
                                                                                                              0:icon_x]

        # merge icon overlay with Output
        Output = IP.mergeImages(icon_overlay, layer2)

        #####################################
        ## Display 2D images using OpenCV ###
        #####################################
        cv2.namedWindow('Video', cv2.WINDOW_FREERATIO)
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Video', Output)
        # cv2.imshow('Cloth Overlay', overlay)

    key = cv2.waitKey(30)
    if key == 27:  # Press esc to break the loop
        break

kinect.close()
cv2.destroyAllWindows()
