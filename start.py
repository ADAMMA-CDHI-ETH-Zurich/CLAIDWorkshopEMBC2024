from claid import CLAID
from claid_designer import CLAIDDesigner
from claid.module.module_factory import ModuleFactory

claid = CLAID()
designer = CLAIDDesigner()
designer.attach(claid)
claid.hello_world()

module_factory = ModuleFactory()
module_factory.register_all_modules_found_in_path("my_modules")
module_factory.register_default_modules()
designer.start("Laptop", "laptop_user", "device", module_factory)