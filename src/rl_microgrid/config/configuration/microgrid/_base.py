from pydantic import BaseModel, ConfigDict
from typing import override


class IConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    @override
    def __getattr__(cls, name):
        """
        Allows accessing the (as default) specified values of the config class as class-level attributes.
        """
        if name in cls.model_fields:
            return cls.model_fields[name].default
        raise AttributeError(f"{name} is not a valid attribute of {cls.__name__}")

    @override
    def model_dump(self, *args, **kwargs):
        """
        Generate a dictionary representation of the config class, optionally specifying which fields to include or exclude.
        The resulting dictionary will contain the attributes of the config class as keys in lowercase, to match the
        constructor parameters of the respective classes expecting the specified attributes.

        Args:
            mode: The mode in which `to_python` should run.
                If mode is 'json', the output will only contain JSON serializable types.
                If mode is 'python', the output may contain non-JSON-serializable Python objects.
            include: A set of fields to include in the output.
            exclude: A set of fields to exclude from the output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to use the field's alias in the dictionary key if defined.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of `None`.
            round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
            warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
                "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
            fallback: A function to call when an unknown value is encountered. If not provided,
                a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError] error is raised.
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A dictionary representation of the model.
        """
        dict = super().model_dump(*args, **kwargs)
        return {key.lower(): value for key, value in dict.items()}
