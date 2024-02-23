from claid import CLAID

from claid.module.module_factory import ModuleFactory

claid = CLAID()

module_factory = ModuleFactory()
claid.start("claid_config.json", "workshop_laptop", "user", "device", module_factory)
