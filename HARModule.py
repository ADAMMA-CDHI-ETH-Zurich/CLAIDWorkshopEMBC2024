import tensorflow.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()


import numpy as np
import pandas as pd

from claid import CLAID
from claid.module import Module

from claid.dispatch.proto.sensor_data_types_pb2 import *
from claid.dispatch.proto.claidservice_pb2 import *

from claid.logger import Logger

class HARModule(Module):

    def __init__(self):
        super().__init__()

    def initialize(self, properties):

        self.subscribe("InputData", AccelerationData(), self.on_data)
        self.output_channel = self.publish("OutputData", StringArray())

        self.required_samples = 10 * 20 # 10 seconds times 20 Hertz
        # 1 person, 200 samples (10 * 20Hz), 3 axis
        self.acceleration_data = np.zeros((1,200,3))
        self.xs = list()
        self.ys = list()
        self.zs = list()

        # Load the model
        self.model_path = 'models/frozen_model.pb'
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
        self.input_tensor = self.graph.get_tensor_by_name('inputs:0')  # Replace with your input tensor name
        self.output_tensor = self.graph.get_tensor_by_name('y_:0')  # Replace with your output tensor name


           


    def on_data(self, data):

        acceleration_data = data.get_data()

        for sample in acceleration_data.samples:
            self.xs.append(sample.acceleration_x*9.80655)
            self.ys.append(sample.acceleration_y*9.80655)
            self.zs.append(sample.acceleration_z*9.80655)

        if len(self.xs) > self.required_samples:
            self.xs = self.xs[-self.required_samples:]
            self.ys = self.ys[-self.required_samples:]
            self.zs = self.zs[-self.required_samples:]

            self.run_inference()

            self.xs.clear()
            self.ys.clear()
            self.zs.clear()

    def run_inference(self):
        # Downstairs	Jogging	  Sitting	Standing	Upstairs	Walking
        # Generate random float data
        Logger.log_info("Running inference")
        test_data = np.zeros((1, 200, 3))
        test_data[0, :, 0] = np.array(self.xs)
        test_data[0, :, 1] = np.array(self.ys)
        test_data[0, :, 2] = np.array(self.zs)

        input_data = test_data

        # Run inference
        print("run sess")
        output_data = self.session.run(self.output_tensor, feed_dict={self.input_tensor: input_data})

        labels = ["Downstairs", "Jogging", "Sitting", "Standing", "Upstairs", "Walking"]
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



