import numpy as np
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import utils_PyKinectV2 as utils
from open3d import *


def initializeKinect():
    kinectVar = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body |
                                                PyKinectV2.FrameSourceTypes_Color)

    return kinectVar


def getDepthDimension(kinect):
    width = kinect.depth_frame_desc.Width  # Default: 512
    height = kinect.depth_frame_desc.Height  # Default: 424

    return width, height


def getColorDimension(kinect):
    width = kinect.color_frame_desc.Width  # Default: 1920
    height = kinect.color_frame_desc.Height  # Default: 1080

    return width, height


def getKinectFrames(kinect, color_height, color_width, color_space):
    body_frame = kinect.get_last_body_frame()
    color_frame = kinect.get_last_color_frame()

    color_img = color_frame.reshape((color_height, color_width, 4)).astype(np.uint8)

    if color_space:
        joint, joint_points = utils.define_joints_and_joint_points_color(body_frame, kinect)
    else:
        joint, joint_points = utils.define_joints_and_joint_points_depth(body_frame, kinect)

    return color_img, joint, joint_points


def alignDepthColor(kinect, color_img):
    align_color_img = utils.get_align_color_image(kinect, color_img)

    return align_color_img


def getBodyJoints(joint, jointpoints):
    joint2D = utils.get_joint2D(joint, jointpoints)

    return joint2D


def drawJoints(image, joint2D):
    out_image = utils.draw_joint2D(image, joint2D, utils.colors_order[0])

    return out_image
