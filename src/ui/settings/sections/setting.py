from abc import ABC, abstractmethod


class Setting(ABC):
    """Defines the interface for a settings dialog section."""

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def add_to_layout(self, layout) -> None:
        pass
