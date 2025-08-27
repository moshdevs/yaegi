from dataclasses import dataclass, field

@dataclass
class House:
    number: int
    lord: str
    rashi: int
    degree: float
    planets: list[str] = field(default_factory=list)
    cusp: float = 0.0

    @property
    def is_occupied(self) -> bool:
        return len(self.planets) > 0

    @property
    def planet_count(self) -> int:
        return len(self.planets)

    def add_planet(self, planet_name: str) -> None:
        if planet_name not in self.planets:
            self.planets.append(planet_name)

    def remove_planet(self, planet_name: str) -> None:
        if planet_name in self.planets:
            self.planets.remove(planet_name)

    def to_dict(self) -> dict[str, any]:
        return {
            "number": self.number,
            "lord": self.lord,
            "rashi": self.rashi,
            "degree": self.degree,
            "planets": self.planets,
            "cusp": self.cusp,
            "is_occupied": self.is_occupied,
            "planet_count": self.planet_count,
        }
      
