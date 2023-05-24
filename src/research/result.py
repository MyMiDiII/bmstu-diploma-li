from dataclasses import dataclass, field

@dataclass
class Result:
    distribution : str
    model        : str
    keys_size    : int
    build_time   : int
    find_time    : float
    bytes_size   : int
    mae          : float

@dataclass
class Results:
    model_name  : str
    keys_sizes  : list[int] = field(default_factory=list)
    build_times : list[int] = field(default_factory=list)
    find_times  : list[float] = field(default_factory=list)
    bytes_sizes : list[int] = field(default_factory=list)
    maes        : list[float] = field(default_factory=list)

    def add(self, result: Result):
        self.keys_sizes.append(result.keys_size)
        self.build_times.append(result.build_time)
        self.find_times.append(result.find_time)
        self.bytes_sizes.append(result.bytes_size)
        self.maes.append(result.mae)

