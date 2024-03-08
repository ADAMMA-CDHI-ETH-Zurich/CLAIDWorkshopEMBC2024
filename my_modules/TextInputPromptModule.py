from claid.module import Module

from datetime import datetime, timedelta

class TextInputPromptModule(Module):

    @staticmethod
    def annotate_module(annotator):
        annotator.set_module_category("UserInput")
        annotator.set_module_description("A Module allowing to post text from the command prompt to a Channel.")
    
        annotator.describe_publish_channel("OutputText", str(), "Channel where inputted text will be posted to.")

    def __init__(self):
        super().__init__()

    def initialize(self, properties):
        print("MyModule Hello!")
        self.output_channel = self.publish("OutputText", str())

        self.register_scheduled_function("InputPrompt", datetime.now() + timedelta(milliseconds=3000), self.prompt_input)

    def prompt_input(self):
        text = input("Input your text: ")

        if text == "":
            return
        
        print("Outputting text ", text)
        self.output_channel.post(text)
        self.register_scheduled_function("InputPrompt", datetime.now() + timedelta(milliseconds=1000), self.prompt_input)



