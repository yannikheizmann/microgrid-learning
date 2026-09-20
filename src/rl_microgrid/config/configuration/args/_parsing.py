from __future__ import annotations
import argparse
from enum import Enum
from pydantic_core import PydanticUndefined
from typing import Any, get_type_hints

from ._args import Args, IAdditionalArgs
from ..static import PROJECT_DESCRIPTION


class ArgsParser:
    @classmethod
    def _get_alias_mapping(cls) -> dict[str, str]:
        alias_mapping = {}
        for field_name, field_type_str in Args.__annotations__.items():
            field_info = Args.model_fields[field_name]
            if field_info.alias:
                alias_mapping[field_info.alias] = field_name
        return alias_mapping

    @classmethod
    def _create_args_from_namespace(cls, args: argparse.Namespace) -> Args:
        args_dict = vars(args)

        for alias, field_name in cls._get_alias_mapping().items():
            if alias in args_dict:
                args_dict[field_name] = args_dict.pop(alias)

        for field_name, field_type in get_type_hints(Args).items():
            if issubclass(field_type, IAdditionalArgs):
                args_value = args_dict.get(field_name)
                if isinstance(args_value, list):
                    parsed_dict = cls.parse_additional_args(args_value)
                    args_dict[field_name] = field_type(**parsed_dict)
                elif isinstance(args_value, field_type):
                    continue
                elif isinstance(args_value, dict):
                    args_dict[field_name] = field_type(**parsed_dict)

        args_dict = {k: v for k, v in args_dict.items() if v is not PydanticUndefined}
        return Args.model_validate(args_dict)

    @classmethod
    def parse_additional_args(cls, arg_list: list[str]) -> dict[str, Any]:
        """
        Parse a string of the form "key1=value1,key2=value2" into a dictionary.
        Handles cases with one or more key-value pairs.
        """
        parsed_dict = {}
        for item in arg_list:
            key, val = item.split("=")
            parsed_dict[key] = val
        return parsed_dict

    @classmethod
    def parse(cls) -> Args:
        """
        Class method to parse command-line arguments and return an Args instance.
        """
        parser = argparse.ArgumentParser(description=PROJECT_DESCRIPTION)

        for field_name, field_type in get_type_hints(Args).items():
            field_info = Args.model_fields[field_name]

            choices = None
            if isinstance(field_type, type) and issubclass(field_type, Enum):
                choices = [item.value for item in field_type]

            aliases = [f"--{field_name}"]
            if field_info.alias:
                aliases.append(f"-{field_info.alias}")

            if issubclass(field_type, IAdditionalArgs):
                parser.add_argument(
                    *aliases,
                    type=str,
                    nargs="+",
                    default=field_info.default,
                    help=field_info.description,
                )
            else:
                parser.add_argument(
                    *aliases,
                    type=str,
                    choices=choices,
                    default=field_info.default,
                    help=field_info.description,
                )

        args = parser.parse_args()
        return cls._create_args_from_namespace(args)
