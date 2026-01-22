import numbers

import pandas as pd
import numpy as np
import yaml
from baybe.parameters import SubstanceParameter
from typing import Dict, List, Union

from src.environment_variables.dir_paths import DirPaths
from src.bayakm.parameters import build_param_list

Distance = float
ParamName = str
ParamValue = Union[str, float]
DistanceDictType = Dict[ParamValue, Distance]
OptimalIndexType = Dict[ParamName, int]


class YieldSimulator:
    """Chooses a random combination of parameters and returns yields based on proximity to that
    combination.
    """
    def __init__(self):
        self.target = None
        self.df = None
        self.parameter_dict = self._build_params_dict()
        self.n_params = len(self.parameter_dict)

        self.rows_without_yield = None
        self.dirs = DirPaths()
        self.optimal_dict = self._build_optimal_dict()

    def add_fake_results(self, df: pd.DataFrame, target: str = "Yield") -> pd.DataFrame:
        """Methode for adding fake results to a dataframe.
        Args:
            df: pd.DataFrame with combinations of parameters, to which the yields are added.
            target: default: "Yield", name of the target parameter.
        Returns:
            df_with_yields: The pd.DataFrame with yields.
        """
        self.df = df
        self.target = target

        if self.target not in df.columns:
            df[self.target] = np.nan
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
    ) -> None:
        self.df.at[index, self.target] = _yield

    @staticmethod
    def _declare_optimal_index(value_list: list[str | float]) -> int:
        scaling = len(value_list)
        best_index = int(np.random.random() * scaling)
        return best_index

    @staticmethod
    def _find_distance(optimal_index: int, value_list: list[ParamValue]) -> DistanceDictType:
        distance_dict: DistanceDictType = {}
        optimal_value = value_list[optimal_index]

        for index, value in enumerate(value_list):
            if isinstance(value, numbers.Number):
                if optimal_value != 0.0:
                    denom = optimal_value
                else:
                    denom = 1
                distance = float(abs(optimal_value - value) / denom)
                distance_dict[float(value)] = distance

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
        return float(np.mean(distance_list))

    @staticmethod
    def _generate_yield(score: float, scale: float = 0.5) -> float:
        prob = 1.0 / ( 1.0 + score * scale )
        return max(0.0, min(1.0, prob))

    def _find_rows_without_yield(self) -> List[int]:
        rows_without_yield: List[int] = []
        for index, value in self.df[self.target].items():
            if not self._check_yield(value):
                rows_without_yield.append(index)
        return rows_without_yield

    @staticmethod
    def _check_yield(value: ParamValue | None) -> bool:
        if value is None:
            return False
        if pd.isna(value):
            return False
        if isinstance(value, (float, int)):
            return value != 0.0
        if isinstance(value, str):
            return value != ""
        return False

    def _save_optimal_dict(self, optimal_dict: dict[str, object]) -> None:
        path = self.dirs.return_file_path("config")

        if self.dirs.check_path(path):
            with open(path, "r") as f:
                config_dict = yaml.safe_load(f)

            config_dict["Simulation"] = optimal_dict

            with open(path, "w") as f:
                yaml.dump(config_dict, f)

    def _load_optimal_dict(self) -> dict[str, object] | None:
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
    ) -> dict[str, object]:

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
                chosen_dict[param_name] = param_value

            row_score: float = self._evaluate_combination(chosen_dict)
            _yield = self._generate_yield(row_score)
            self._append_yield(_yield, index)

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
