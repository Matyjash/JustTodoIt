class Setting:
    """
    Represents a single application setting.
    """

    def __init__(self, key: str, value):
        """
        Initialize a Setting.

        Args:
            key: The setting key/name
            value: The setting value
        """
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key}: {self.value}"

    def __repr__(self):
        return f"Setting(key='{self.key}', value={self.value})"
