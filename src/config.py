import os
import yaml
from pathlib import Path
from typing import TypedDict, Optional

class NewsletterConfig(TypedDict):
    """Type definition for individual newsletter configurations."""
    name: str
    query: str
    folder_id: str
    schedule: str
    footer_starts_with: Optional[str]

class AppConfig:
    """Handles loading and managing application-wide settings from YAML."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Load the configuration file.
        :param config_path: Path to the YAML file. Defaults to configs/newsletters.yaml.
        """
        if config_path is None:
            # Locate configs/newsletters.yaml relative to the src directory
            config_path = str(Path(__file__).parent.parent / "configs" / "newsletters.yaml")
        
        self.config_path = config_path
        self._newsletters: list[NewsletterConfig] = []
        self._load_config()

    def _load_config(self) -> None:
        """Parse the YAML file and store newsletter settings."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            self._newsletters = data.get("newsletters", [])

    @property
    def newsletters(self) -> list[NewsletterConfig]:
        """Get the list of registered newsletter configurations."""
        return self._newsletters
