from dataclasses import dataclass, field

@dataclass
class Result:
    distribution : str
    model        : str
    keys_size    : int
    build_time   : int
    find_time    : float
    predict_time : float
    clarify_time : float
    index_size   : int
    model_size   : int
    mean_ae      : float
    max_ae       : float

@dataclass
class Results:
    model_name  : str
    keys_sizes  : list[int] = field(default_factory=list)
    build_times : list[int] = field(default_factory=list)
    find_times  : list[float] = field(default_factory=list)
    predict_times  : list[float] = field(default_factory=list)
    clarify_times  : list[float] = field(default_factory=list)
    index_sizes : list[int] = field(default_factory=list)
    model_sizes : list[int] = field(default_factory=list)
    mean_aes    : list[float] = field(default_factory=list)
    max_aes     : list[float] = field(default_factory=list)

    def add(self, result: Result):
        self.keys_sizes.append(result.keys_size)
        self.build_times.append(result.build_time)
        self.find_times.append(result.find_time)
        self.predict_times.append(result.predict_time)
        self.clarify_times.append(result.clarify_time)
        self.index_sizes.append(result.index_size)
        self.model_sizes.append(result.model_size)
        self.mean_aes.append(result.mean_ae)
        self.max_aes.append(result.max_ae)

