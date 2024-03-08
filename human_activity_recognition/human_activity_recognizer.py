import tensorflow.compat.v1 as tf
tf.compat.v1.disable_v2_behavior()
import numpy as np

class HumanActivityRecognizer():

    def __init__(self):
        super().__init__()
        self.ctr = 0

    def initialize(self):


        self.model_path = 'models/har_model.pb'
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

        self.required_samples = 5 * 20 # 5 seconds times 20 Hertz

    def run_inference(self, acceleration_data, gyroscope_data):
        # Downstairs	Jogging	  Sitting	Standing	Upstairs	Walking
        # Generate random float data
        

        if acceleration_data.shape != (3, self.required_samples):
            raise ValueError("Acceleration data in invalid shape. Required shape {} but got {}.".format((3, self.required_samples), acceleration_data.shape))
        
        if gyroscope_data.shape != (3, self.required_samples):
            raise ValueError("Acceleration data in invalid shape. Required shape {} but got {}.".format((3, self.required_samples), gyroscope_data.shape))
        
        print("Running inference")

        # test_data = np.zeros((1, self.required_samples, 6), dtype=np.float32)
        # test_data[0, :, 0] = np.array(self.acc_xs, dtype=np.float32)
        # test_data[0, :, 1] = np.array(self.acc_ys, dtype=np.float32)
        # test_data[0, :, 2] = np.array(self.acc_zs, dtype=np.float32)
        # test_data[0, :, 3] = np.array(self.gyro_xs, dtype=np.float32)
        # test_data[0, :, 4] = np.array(self.gyro_ys, dtype=np.float32)
        # test_data[0, :, 5] = np.array(self.gyro_zs, dtype=np.float32)
        data = []
        N_SAMPLES = 100
        data.extend(acceleration_data[0,:])
        data.extend(acceleration_data[1,:])
        data.extend(acceleration_data[2,:])
        data.extend(gyroscope_data[0,:])
        data.extend(gyroscope_data[1,:])
        data.extend(gyroscope_data[2,:])

        
        data = np.array(data, dtype=np.float32)
        input_data = data.reshape((1, N_SAMPLES, 6))


        output_data = self.session.run(self.output_tensor, feed_dict={self.input_tensor: input_data})

        # Process the output data as needed
        output_data = output_data[0]

        return output_data 

    def get_label(self, output_data):
        index = np.argmax(output_data)
        return self.get_labels()[index]

    def get_labels(self):
        return ["Jump", "Stand", "Walk"]