from claid.module import Module

class MyModule(Module):
    @staticmethod
    def annotate_module(annotator):
        annotator.set_module_category("UserInput")
        annotator.set_module_description("A Module allowing to post text from the command prompt to a Channel.")
    
        annotator.describe_subscribe_channel("OutputText", str(), "Channel where inputted text will be posted to.")

    def __init__(self):
        super().__init__()

    def initialize(self, properties):
        print("MyModule Hello!")

