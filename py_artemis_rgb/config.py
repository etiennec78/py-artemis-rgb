"""Configuration classes for Artemis RGB client.

This module provides configuration classes used to customize
the behavior of the Artemis RGB client.
"""

from dataclasses import dataclass


@dataclass
class ArtemisConfig:
    """Configuration for Artemis RGB client.

    Attributes:
        ip: IP adress of the device running Artemis RGB
        port: Port used by the Artemis RGB server
    """

    ip: str = "localhost"
    port: int = 9696
