from dataclasses import dataclass


@dataclass
class Coordinates:
    latitude: float
    longitude: float
    not_exists: bool = None

    def __post_init__(self):
        self.not_exists = self.not_exists or (self.latitude is None or self.longitude is None)
