from claid import CLAID
from claid_designer import CLAIDDesigner
from claid.module.module_factory import ModuleFactory


claid = CLAID()

# Do this before importing tensorflow!!
claid.hello_world()


module_factory = ModuleFactory()
module_factory.register_all_modules_found_in_path("my_modules")
module_factory.print_registered_modules()


claid.start("claid_config.json", "Laptop", "laptop_user", "device", module_factory)
