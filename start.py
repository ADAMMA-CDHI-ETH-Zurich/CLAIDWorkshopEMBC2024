from claid import CLAID

from claid.module.module_factory import ModuleFactory

from HARModule import HARModule

claid = CLAID()

module_factory = ModuleFactory()
module_factory.register_module(HARModule)
claid.start("claid_config.json", "workshop_laptop", "user", "device", module_factory)
