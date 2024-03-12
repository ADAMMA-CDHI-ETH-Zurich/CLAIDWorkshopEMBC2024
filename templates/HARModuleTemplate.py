import tensorflow.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()


import numpy as np

from claid import CLAID
from claid.module import Module

from claid.dispatch.proto.sensor_data_types_pb2 import *
from claid.dispatch.proto.claidservice_pb2 import *

from claid.logger import Logger

from human_activity_recognition.human_activity_recognizer import HumanActivityRecognizer

import cv2

class HARModule(Module):
    @staticmethod
    def annotate_module(annotator):
        annotator.set_module_category("Custom")
        annotator.set_module_description("A Module allowing to do human activity recognition using machine learning.")
    
        annotator.describe_subscribe_channel("AccelerationInputData", AccelerationData(), "Acceleration input data")
        annotator.describe_subscribe_channel("GyroscopeInputData", GyroscopeData(), "Gyroscope input data")
        annotator.describe_publish_channel("OutputDataLabel", str(), "Output data")


    def __init__(self):
        super().__init__()
        self.ctr = 0

    def initialize(self, properties):

        self.subscribe("AccelerationInputData", AccelerationData(), self.on_acceleration_data)
        self.subscribe("GyroscopeInputData", GyroscopeData(), self.on_gyroscope_data)

        self.output_channel = self.publish("OutputDataLabel", str())

        self.required_samples = 5 * 20 # 5 seconds times 20 Hertz
        # 1 person, 200 samples (10 * 20Hz), 3 axis
        self.acc_xs = list()
        self.acc_ys = list()
        self.acc_zs = list()

        self.gyro_xs = list()
        self.gyro_ys = list()
        self.gyro_zs = list()

        self.recognizer = HumanActivityRecognizer()
        self.recognizer.initialize_recognizer()

        

    def on_acceleration_data(self, data):
        # ... your code
        pass

    def on_gyroscope_data(self, data):
        # ... your code
        pass

    def run_inference_if_enough_data(self):
        # Downstairs	Jogging	  Sitting	Standing	Upstairs	Walking
        # Generate random float data
        print("running inference ", len(self.acc_xs), len(self.gyro_xs))

        # if(len(self.acc_xs) >= self.required_samples and len(self.gyro_xs) >= self.required_samples):

            # Make sure both acceleration and gyroscope data have shape [3, 200]
            # output_data = self.recognizer.run_inference(your_acceleration_data,\
            #                                             your_gyroscope_data)
            # label = self.recognizer.get_label(output_data)
