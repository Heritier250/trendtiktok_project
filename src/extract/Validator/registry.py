from typing import Dict, List , Type
from .base import SecurityCheck


class CheckRegistry:
    _checks:Dict[str, Type[SecurityCheck]] = {}
    @classmethod
    def register(cls, check_class: Type[SecurityCheck]) -> None:
        if not issubclass(check_class, SecurityCheck):
            raise TypeError(f"{check_class} must inhert from security")
        cls._checks[check_class.__name__] = check_class
    @classmethod
    def get_check(cls, name: str) -> Type[SecurityCheck]:
            return cls._checks.get(name)
    @classmethod
    def get_enabled_checks(cls, enabled_names: List[str]) ->List[Type[SecurityCheck]]:
        enabled = []
        for name in enabled_names:
            check_class=cls._checks.get(name)
            if check_class:
                enabled.append(check_class)
        return enabled 
    @classmethod
    def clear(cls) -> None:
        cls._checks.clear()       