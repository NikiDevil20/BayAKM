import pandas as pd
from typing import Callable
import numpy as np
import yaml
from baybe.parameters import SubstanceParameter

from src.environment_variables.dir_paths import DirPaths
from src.bayakm.parameters import build_param_list

Distance = float
ParamName = str
ParamValue = str | float
DistanceDictType = dict[ParamValue, Distance]
OptimalIndexType = dict[ParamName, int]


class YieldSimulator:
    def __init__(self):
        self.target = None
        self.df = None
        self.parameter_dict = self._build_params_dict()
        self.n_params = len(self.parameter_dict)

        self.rows_without_yield = None
        self.dirs = DirPaths()
        self.optimal_dict = self._build_optimal_dict()

    def add_fake_results(self, df: pd.DataFrame, target: str = "Yield"):
        self.df = df
        if "Yields" not in df.columns:
            df["Yield"] = np.nan
        self.target = target
        self.rows_without_yield = self._find_rows_without_yield()


        return self._iterate_df()

    @staticmethod
    def _build_params_dict():
        params_with_type = build_param_list()
        parameter_dict = {}
        for parameter in params_with_type:
            if isinstance(parameter, SubstanceParameter):
                parameter_dict[parameter.name] = list(parameter.data.keys())
            else:
                parameter_dict[parameter.name] = list(parameter.values)

        return parameter_dict



    def _append_yield(
            self,
            _yield: float,
            index: int
    ) -> pd.DataFrame:
        df = self.df
        df.loc[index, "Yield"] = _yield
        return df

    @staticmethod
    def _declare_optimal_index(value_list: list[str | float]) -> int:
        scaling = len(value_list)
        best_index = int(np.random.random() * scaling)
        return best_index

    @staticmethod
    def _find_distance(optimal_index: int, value_list: list[str | float]) -> DistanceDictType:
        distance_dict = {}
        optimal_value = value_list[optimal_index]

        for index, value in enumerate(value_list):
            if isinstance(value, float) or isinstance(value, int):
               distance_dict[float(value)] = float(abs(optimal_value - value) / optimal_value)

            if isinstance(value, str):
                distance_dict[value] = float(abs(optimal_index - index))

        return distance_dict

    def _get_values_from_current_row(self, row_index: int) -> dict[ParamName, ParamValue]:
        df = self.df
        parameter_dict = self.parameter_dict
        chosen_params = {}
        for param_name in parameter_dict.keys():
            param_value = df[param_name][row_index]
            chosen_params[param_name] = param_value

        return chosen_params

    def _evaluate_combination(self, chosen: dict[ParamName, ParamValue]) -> float:
        distance_list = []
        optimal_dict = self.optimal_dict
        distance_dict: DistanceDictType = optimal_dict["distance_dict"]
        for param in chosen.keys():
            distance = distance_dict[param][chosen[param]]
            distance_list.append(distance)

        return self._generate_score(distance_list)

    @staticmethod
    def _generate_score(distance_list: list[float]) -> float:
        total: float = 0.0
        for distance in distance_list:
            total += distance

        return total / len(distance_list)

    @staticmethod
    def _generate_yield(score: float, scale: float = 0.5) -> float:
        prob = 1.0 / ( 1.0 + score * scale )
        return max(0.0, min(1.0, prob))

    def _find_rows_without_yield(self) -> list[int]:
        rows_without_yield = []
        for row in self.df.itertuples():
            yield_value: str | int | float = row[-1]
            if not self._check_yield(yield_value):
                row_index = row[0]
                rows_without_yield.append(row_index)
        return rows_without_yield

    @staticmethod
    def _check_yield(value: float | str | None) -> bool:
        if isinstance(value, float) and value != 0.0:
            if not np.isnan(value):
                return True
        if isinstance(value, int) and value != 0:
            return True
        if isinstance(value, str) and value != "":
            return True
        return False

    def _save_optimal_dict(self, optimal_dict: dict[str, OptimalIndexType | DistanceDictType]) -> None:
        path = self.dirs.return_file_path("config")

        if self.dirs.check_path(path):
            with open(path, "r") as f:
                config_dict = yaml.safe_load(f)

            config_dict["Simulation"] = optimal_dict

            with open(path, "w") as f:
                yaml.dump(config_dict, f)

    def _load_optimal_dict(self) -> dict[str, OptimalIndexType | DistanceDictType] | None:
        path = self.dirs.return_file_path("config")

        if self.dirs.check_path(path):
            with open(path, "r") as f:
                config_dict = yaml.safe_load(f)
            if "Simulation" in config_dict.keys():
                optimal_indices = config_dict["Simulation"]
                return optimal_indices
            else:
                return None
        else:
            return None

    def _build_optimal_dict(
            self,
    ) -> dict[str, OptimalIndexType | DistanceDictType]:

        parameter_dict = self.parameter_dict
        optimal_dict: dict[str, OptimalIndexType | dict[str, DistanceDictType]] = self._load_optimal_dict()

        if optimal_dict is None:
            optimal_dict = {
                "optimal_indices": {},
                "distance_dict": {}
            }
            for parameter in parameter_dict.keys():
                value_list = parameter_dict[parameter]

                optimal_index = self._declare_optimal_index(value_list)
                distance_dict = self._find_distance(optimal_index, value_list)

                optimal_dict["optimal_indices"][parameter] = optimal_index
                optimal_dict["distance_dict"][parameter] = distance_dict  # Type:ignore

        self._save_optimal_dict(optimal_dict)
        return optimal_dict

    def _iterate_df(self):
        df = self.df
        param_names = self.parameter_dict.keys()
        rows_without_yield = self._find_rows_without_yield()
        yield_dict: dict[int, float] = {}

        for index in rows_without_yield:
            chosen_dict: dict[ParamName, ParamValue] = {}
            for param_name in param_names:
                param_value: ParamValue = df[param_name][index]
                chosen_dict[param_name]: ParamValue = param_value

            row_score: float = self._evaluate_combination(chosen_dict)
            _yield = self._generate_yield(row_score)
            df = self._append_yield(_yield, index)

        return df



if __name__ == "__main__":
    _df = pd.DataFrame(
        {
            "Parameter_1": [1, 2, 3, 4],
            "Parameter_2": ["Hexan", "Pentan", "Butan", "Propan"],
            "Yield": [0.6, np.nan, "", 0.0]
        }
    )
    _dict = {
        "Parameter_1": [1, 2, 3, 4],
        "Parameter_2": ["Hexan", "Pentan", "Butan", "Propan"],
    }
    sim = YieldSimulator()
    sim._build_params_dict()
    print(sim.parameter_dict)
    print(sim.optimal_dict)
