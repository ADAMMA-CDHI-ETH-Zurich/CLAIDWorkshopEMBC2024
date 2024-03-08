import tensorflow.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()


import numpy as np

from claid import CLAID
from claid.module import Module

from claid.dispatch.proto.sensor_data_types_pb2 import *
from claid.dispatch.proto.claidservice_pb2 import *

from claid.logger import Logger

import cv2

class HARModule(Module):

    def __init__(self):
        super().__init__()
        self.ctr = 0

    def initialize(self, properties):

        self.subscribe("AccelerationInputData", AccelerationData(), self.on_acceleration_data)
        self.subscribe("GyroscopeInputData", GyroscopeData(), self.on_gyroscope_data)

        self.output_channel = self.publish("OutputData", StringArray())

        self.required_samples = 5 * 20 # 5 seconds times 20 Hertz
        # 1 person, 200 samples (10 * 20Hz), 3 axis
        self.acc_xs = list()
        self.acc_ys = list()
        self.acc_zs = list()

        self.gyro_xs = list()
        self.gyro_ys = list()
        self.gyro_zs = list()

        # Load the model
        self.model_path = 'models/100_20_6_3_nomagnew.pb'
        self.graph = tf.Graph()


        with self.graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # Start a session
        self.session = tf.Session(graph=self.graph)
        # Get the input and output tensors by name
        self.input_tensor = self.graph.get_tensor_by_name('LSTM_1_input:0')  # Replace with your input tensor name
        self.output_tensor = self.graph.get_tensor_by_name('Dense_2/Softmax:0')  # Replace with your output tensor name

        cv2.namedWindow("ClassificationView", cv2.WINDOW_AUTOSIZE) 


        

    def on_acceleration_data(self, data):

        acceleration_data = data.get_data()

        for sample in acceleration_data.samples:
            self.acc_xs.append(np.float32(sample.acceleration_x))
            self.acc_ys.append(np.float32(sample.acceleration_y))
            self.acc_zs.append(np.float32(sample.acceleration_z))

        if len(self.acc_xs) > self.required_samples:
            self.acc_xs = self.acc_xs[-self.required_samples:]
            self.acc_ys = self.acc_ys[-self.required_samples:]
            self.acc_zs = self.acc_zs[-self.required_samples:]


     

        self.run_inference_if_enough_data()

    def on_gyroscope_data(self, data):

        gyroscope_data = data.get_data()

        for sample in gyroscope_data.samples:
            self.gyro_xs.append(np.float32(sample.gyroscope_x))
            self.gyro_ys.append(np.float32(sample.gyroscope_y))
            self.gyro_zs.append(np.float32(sample.gyroscope_z))

        if len(self.gyro_xs) > self.required_samples:
            self.gyro_xs = self.gyro_xs[-self.required_samples:]
            self.gyro_ys = self.gyro_ys[-self.required_samples:]
            self.gyro_zs = self.gyro_zs[-self.required_samples:]


        

        self.run_inference_if_enough_data()

    def run_inference_if_enough_data(self):
        # Downstairs	Jogging	  Sitting	Standing	Upstairs	Walking
        # Generate random float data
        
        print("running inference ", len(self.acc_xs), len(self.gyro_xs))
        if(len(self.acc_xs) >= self.required_samples and len(self.gyro_xs) >= self.required_samples):

            Logger.log_info("Running inference")
            # test_data = np.zeros((1, self.required_samples, 6), dtype=np.float32)
            # test_data[0, :, 0] = np.array(self.acc_xs, dtype=np.float32)
            # test_data[0, :, 1] = np.array(self.acc_ys, dtype=np.float32)
            # test_data[0, :, 2] = np.array(self.acc_zs, dtype=np.float32)
            # test_data[0, :, 3] = np.array(self.gyro_xs, dtype=np.float32)
            # test_data[0, :, 4] = np.array(self.gyro_ys, dtype=np.float32)
            # test_data[0, :, 5] = np.array(self.gyro_zs, dtype=np.float32)
            data = []
            N_SAMPLES = 100
            data.extend(self.acc_xs[:N_SAMPLES])
            data.extend(self.acc_ys[:N_SAMPLES])
            data.extend(self.acc_zs[:N_SAMPLES])
            data.extend(self.gyro_xs[:N_SAMPLES])
            data.extend(self.gyro_xs[:N_SAMPLES])
            data.extend(self.gyro_xs[:N_SAMPLES])

            
            data = np.array(data, dtype=np.float32)
            input_data =  data.reshape((1, N_SAMPLES, 6))

            # Run inference
            print("run sess")
            output_data = self.session.run(self.output_tensor, feed_dict={self.input_tensor: input_data})

            labels = ["Jump", "Stand", "Walk"]
            # Process the output data as needed
            output_data = output_data[0]
            index = np.argmax(output_data)
            print("CLASSIFICATION RESULT", labels[index])

            labels_score = list()
            labels_score.append(str(labels[index]))
            labels_score.append(str(output_data[index]))
            for score in output_data:
                labels_score.append(str(score))

            output = StringArray(val=labels_score)
            print("Posting to output channel")
            self.output_channel.post(output)

            # self.acc_xs = self.acc_xs[-50:]
            # self.acc_ys = self.acc_ys[-50:]
            # self.acc_zs = self.acc_zs[-50:]

            # self.gyro_xs = self.gyro_xs[-50:]
            # self.gyro_ys = self.gyro_ys[-50:]
            # self.gyro_zs = self.gyro_zs[-50:]

            self.acc_xs.clear()
            self.acc_ys.clear()
            self.acc_zs.clear()
            self.gyro_xs.clear()
            self.gyro_ys.clear()
            self.gyro_zs.clear()

            image = 0 * 1 + np.zeros((300, 300, 3), dtype=np.uint8)

            # label = ""
            # if output_data[index] > 0.9:
            #     label = labels[index]
            # else:
            #     label = "Standing"
            label = labels[index]

            # Create a named window with size 300x300

            # Get the text size to calculate the position for centering
            text = label + " " + str(output_data[index])
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

            # Calculate the position to center the text
            text_position = ((300 - text_size[0]) // 2, (300 + text_size[1]) // 2)

            # Put the text in the center of the image
            cv2.putText(image, text, text_position, font, font_scale, (255, 255, 255), font_thickness)

            # Display the image in the named window
            cv2.imshow("ClassificationView", image)

            # Wait for a key event and close the window when a key is pressed
            cv2.waitKey(1)
            self.ctr += 1