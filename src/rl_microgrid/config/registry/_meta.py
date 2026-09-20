from abc import ABCMeta

from ._registry import Registry


class RegistryMeta(ABCMeta):
    _interface_name: str = ""
    _suffix: str = ""

    def __class_getitem__(cls, interface_name: str):
        """Pass the full interface name like 'IAgent', 'IBrain', etc."""
        if not interface_name.startswith("I"):
            raise ValueError(f"Interface name must start with 'I', got {interface_name}.")
        suffix = interface_name[1:]

        class CustomMeta(RegistryMeta):
            _interface_name = interface_name
            _suffix = suffix

        return CustomMeta

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not cls._suffix or not cls._interface_name:
            return
        if name == cls._interface_name:
            return
        if not name.endswith(cls._suffix):
            raise ValueError(f"Class name '{name}' must end with '{cls._suffix}'.")
        registered_name = name[: -len(cls._suffix)]
        Registry.register(cls._interface_name, registered_name, cls)
