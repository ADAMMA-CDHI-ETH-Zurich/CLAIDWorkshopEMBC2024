import tensorflow.compat.v1 as tf
import numpy as np
import pandas as pd



def load_csv_data(file_path, N):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, header=None, names=['id', 'label', 'timestamp', 'x', 'y', 'z'])

    # Retrieve data from the first N rows
    data = df.head(N)

    return data


tf.compat.v1.disable_v2_behavior()

# Load the model
model_path = 'models/frozen_model.pb'
graph = tf.Graph()

data = load_csv_data("data.txt", 200)
data = data.to_numpy()
test_data = data[:, 3:]

with graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(model_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Start a session
with tf.Session(graph=graph) as sess:
    # Get the input and output tensors by name
    input_tensor = graph.get_tensor_by_name('inputs:0')  # Replace with your input tensor name
    output_tensor = graph.get_tensor_by_name('y_:0')  # Replace with your output tensor name


    # Downstairs	Jogging	  Sitting	Standing	Upstairs	Walking
    # Generate random float data
    input_data = [test_data]

    # Run inference
    output_data = sess.run(output_tensor, feed_dict={input_tensor: input_data})

    # Process the output data as needed
    print(output_data)

