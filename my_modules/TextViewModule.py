from claid.module import Module
from claid.dispatch.proto.sensor_data_types_pb2 import *
from claid.dispatch.proto.claidservice_pb2 import *

from datetime import datetime, timedelta
import cv2
import numpy as np

# This is a template for a minimalistic Module in CLAID.
class TextViewModule(Module):
    @staticmethod
    def annotate_module(annotator):
        annotator.set_module_category("Custom")
        annotator.set_module_description("A Module allowing to show text in a window")
        
        annotator.describe_subscribe_channel("InputData", str(), "Input text")


    def __init__(self):
        super().__init__()

    def initialize(self, properties):

        self.input_channel = self.subscribe("InputData", str(), self.on_data)
        cv2.namedWindow("TextView", cv2.WINDOW_AUTOSIZE) 
        image = 0 * 1 + np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.imshow("TextView", image)

    def on_data(self, data):
        
        text = data.get_data()

        # Get the text size to calculate the position for centering
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

        # Calculate the position to center the text
        text_position = ((300 - text_size[0]) // 2, (300 + text_size[1]) // 2)
        image = 0 * 1 + np.zeros((300, 300, 3), dtype=np.uint8)

        # Put the text in the center of the image
        cv2.putText(image, text, text_position, font, font_scale, (255, 255, 255), font_thickness)

        # Display the image in the named window
        cv2.imshow("TextView", image)

        # Wait for a key event and close the window when a key is pressed
        cv2.waitKey(1)