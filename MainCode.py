import cv2
import math as mt
import Kinect as Kv2
import ImageProcessing as IP
import numpy as np

disconnectStatus = 0


def StartKinect():
    #############################
    ### Kinect runtime object ###
    #############################
    shoulder_distance = 100
    overlay = 0

    SJR_x = 0
    SJR_y = 0
    SJL_x = 0
    SJL_y = 0
    Nk_x = 0
    Nk_y = 0

    kinect = Kv2.initializeKinect()

    depth_width, depth_height = Kv2.getDepthDimension(kinect)
    color_width, color_height = Kv2.getColorDimension(kinect)

    shirt_img = cv2.imread("Datasets/2D Cloths self made/shirt3.png", -1)
    shirt_img_gray = cv2.cvtColor(shirt_img, cv2.COLOR_BGR2GRAY)

    ########################
    ### Main Kinect Loop ###
    ########################

    while True:

        if kinect.has_new_body_frame() \
                and kinect.has_new_body_index_frame() \
                and kinect.has_new_color_frame() \
                and kinect.has_new_depth_frame() \
                and kinect.has_new_infrared_frame():

            ##############################
            ### Get images from camera ###
            ##############################
            print("running")
            body_index_img, color_img, depth_img, infrared_img, joint, jointpoints = Kv2.getKinectFrames(kinect,
                                                                                                         depth_height,
                                                                                                         depth_width,
                                                                                                         color_height,
                                                                                                         color_width)

            align_color_img = Kv2.alignDepthColor(kinect, color_img)
            Bk_removed = IP.removeBackground(align_color_img, body_index_img)

            cropped_cloth = IP.removeClothBK(shirt_img_gray, shirt_img)

            #################################################
            ### Extract and Draw 2D joints on single body ###
            #################################################

            if joint != 0:

                joint2D, joint3D = Kv2.getBodyJoints(joint, jointpoints, depth_img, depth_width, depth_height)
                SJR_x, SJR_y, SJL_x, SJL_y, Nk_x, Nk_y = joint2D[8, 0], joint2D[8, 1], joint2D[4, 0], joint2D[4, 1], joint2D[2, 0], joint2D[2, 1]

                # print("Shoulder Right coordinates: " + str(joint2D[8]))
                # print("Shoulder Left coordinates: " + str(joint2D[4]))

                Bk_removed = Kv2.drawJoints(Bk_removed, joint2D)
                distance = mt.sqrt(mt.pow(SJL_x - SJR_x, 2))

            else:
                distance = 100

            if distance <= 0:
                shoulder_distance = shoulder_distance
            else:
                shoulder_distance = distance

            # print("Shoulder Distance: " + str(shoulder_distance))

            ##############################################
            ### Resizing Cloth image according to user ###
            ##############################################

            resized_cloth = IP.image_resize(cropped_cloth, width=int(shoulder_distance + 60))
            cloth_row = np.shape(resized_cloth)[0]
            cloth_col = np.shape(resized_cloth)[1]

            #####################################################
            ### Add resized image to Background removed Image ###
            #####################################################

            # Offsets:
            SJL_y = int(SJL_y - 20)
            SJL_x = int(SJL_x - 20)
            Nk_x = int(Nk_x - (shoulder_distance / 2) - 30)

            if SJL_y >= 0 and SJL_x >= 0:
                overlay = np.zeros_like(Bk_removed)
                overlay[Nk_y:Nk_y + cloth_row, Nk_x:Nk_x + cloth_col] = resized_cloth[0:cloth_row, 0:cloth_col]
                cv2.addWeighted(overlay, 1, Bk_removed, 1, 0, Bk_removed)

            #####################################
            ## Display 2D images using OpenCV ###
            #####################################

            cv2.imshow('Color + Depth Image', align_color_img)  # (512, 424, 4)
            cv2.imshow('Removed Background', Bk_removed)
            cv2.imshow('overlay', overlay)

        key = cv2.waitKey(30)
        if disconnectStatus == 1:
            break

    kinect.close()
    cv2.destroyAllWindows()
    print("Kinect Shutdown!")
