from claid import CLAID

from claid.module.module_factory import ModuleFactory


claid = CLAID()
# Do this before importing tensorflow!!
claid.hello_world()

from HARModule import HARModule

module_factory = ModuleFactory()
module_factory.register_module(HARModule)
claid.start("claid_config.json", "workshop_laptop", "user", "device", module_factory)
