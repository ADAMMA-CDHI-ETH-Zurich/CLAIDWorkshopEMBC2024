from claid.module import Module

class MyModule(Module):

    def __init__(self):
        super().__init__()

    def initialize(self, properties):
        print("MyModule Hello!")

    def annotate_module(annotator):
        annotator.set_module_description("Just a test Module")