from typing import Type


class Registry:
    _registries: dict[str, dict[str, Type]] = {}

    @classmethod
    def register(cls, interface_name: str, name: str, item: Type) -> None:
        if interface_name not in cls._registries:
            cls._registries[interface_name] = {}
        if name in cls._registries[interface_name]:
            raise ValueError(f"{name} already registered under {interface_name}.")
        cls._registries[interface_name][name] = item

    @classmethod
    def get(cls, interface_name: str, name: str) -> Type:
        if interface_name not in cls._registries:
            raise ValueError(f"No registry found for {interface_name}.")
        if name not in cls._registries[interface_name]:
            raise ValueError(
                f"{name} not registered under {interface_name}. Registered classes are {list(cls._registries[interface_name].keys())}."
            )
        return cls._registries[interface_name][name]

    @classmethod
    def get_all(cls, interface_name: str) -> dict[str, Type]:
        if interface_name not in cls._registries:
            raise ValueError(f"No registry found for {interface_name}.")
        return dict(cls._registries[interface_name])
