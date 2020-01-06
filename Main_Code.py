import cv2
import math as mt
import Kinect as Kv2
import ImageProcessing as IP

#############################
### Kinect runtime object ###
#############################

kinect = Kv2.initializeKinect()

depth_width, depth_height = Kv2.getDepthDimension(kinect)
color_width, color_height = Kv2.getColorDimension(kinect)

shirt_img = cv2.imread("Datasets/2D Cloths self made/shirt3.png")
shirt_img_gray = cv2.imread("Datasets/2D Cloths self made/shirt3.png", 0)

#################
### Main Loop ###
#################

while True:

    if kinect.has_new_body_frame() \
            and kinect.has_new_body_index_frame() \
            and kinect.has_new_color_frame() \
            and kinect.has_new_depth_frame() \
            and kinect.has_new_infrared_frame():

        ##############################
        ### Get images from camera ###
        ##############################

        body_index_img, color_img, depth_img, infrared_img, joint, jointpoints = Kv2.getKinectFrames(kinect, depth_height, depth_width, color_height, color_width)

        align_color_img = Kv2.alignDepthColor(kinect, color_img)
        Bk_removed = IP.removeBackground(align_color_img, body_index_img)

        cropped_cloth = IP.removeClothBK(shirt_img_gray, shirt_img)

        #################################################
        ### Extract and Draw 2D joints on single body ###
        #################################################

        if joint != 0:

            joint2D, joint3D = Kv2.getBodyJoints(joint, jointpoints, depth_img, depth_width, depth_height)
            SJR_x, SJR_y, SJL_x, SJL_y = joint2D[8, 0], joint2D[8, 1], joint2D[4, 0], joint2D[4, 1]

            print("Shoulder Right coordinates: " + str(joint2D[8]))
            print("Shoulder Left coordinates: " + str(joint2D[4]))

            Bk_removed = Kv2.drawJoints(Bk_removed, joint2D)
            distance = mt.sqrt(mt.pow(SJL_x - SJR_x, 2))

        else:
            distance = 100

        if distance <= 0:
            shoulder_distance = shoulder_distance
        else:
            shoulder_distance = distance

        print("Shoulder Distance: " + str(shoulder_distance))

        ##############################################
        ### Resizing Cloth image according to user ###
        ##############################################



        #####################################################
        ### Add resized image to Background removed Image ###
        #####################################################

        resized_cloth = IP.resizeCloths(shoulder_distance, cropped_cloth)

        ######################################
        ### Display 2D images using OpenCV ###
        ######################################

        cv2.imshow('Color + Depth Image', align_color_img)  # (512, 424, 4)
        cv2.imshow('Removed Background', Bk_removed)
        cv2.imshow('Shirt', resized_cloth)

    key = cv2.waitKey(30)
    if key == 27:  # Press esc to break the loop
        break

kinect.close()
cv2.destroyAllWindows()
