from claid.module import Module
from claid.dispatch.proto.sensor_data_types_pb2 import *
from claid.dispatch.proto.claidservice_pb2 import *

from datetime import datetime, timedelta

# This is a template for a minimalistic Module in CLAID.
class MyCustomModule(Module):
    @staticmethod
    def annotate_module(annotator):
        annotator.set_module_category("Custom")
        annotator.set_module_description("A Module allowing to post text from the command prompt to a Channel.")
    
        annotator.describe_subscribe_channel("InputData", AccelerationData(), "Input data")
        annotator.describe_publish_channel("OutputData", str(), "Output data")

        annotator.describe_property("threshold", "Threshold for the activity recognition.")

    def __init__(self):
        super().__init__()

    def initialize(self, properties):
        print("MyModule Hello!")

        self.threshold = properties["threshold"]

        # Here you can publish/subscribe Channels:
        self.input_channel = self.subscribe("InputChannel", AccelerationData(), self.on_data)
        self.output_channel = self.publish("OutputChannel", str())

        # Or, you can register periodic or scheduled functions:
        # Register a function which will be executed repeatedly every 2 seconds:
        self.register_periodic_function("MyFunctionName", self.my_periodic_function, timedelta(seconds=2))
        # Register a function which will be executed once at an exact time, e.g., in 10 seconds from now.
        self.register_scheduled_function("MyScheduledFunction", self.my_scheduled_function, datetime.now() + timedelta(seconds=10))

    # This function is called whenever there is any new data on the InputChannel. 
    def on_data(self, data):
        data = data.getData()

    # This function is called periodically based on the intervall specified above (e.g., 2 seconds).
    def my_periodic_function(self):
        print("Periodic function called")

    # This function is called once at a specific time.
    def my_scheduled_function(self):
        print("Scheduled function called")

        # If you want, you can register the function to be executed again at a later time.
        # self.register_scheduled_function("MyScheduledFunction", self.my_scheduled_function, datetime.now() + timedelta(seconds=10))
