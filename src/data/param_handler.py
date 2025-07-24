import yaml
from ..bayakm.dir_paths import DirPaths
import os
from baybe.parameters import SubstanceParameter


class ParamHandler:
    def __init__(self):
        pt = DirPaths()
        self.param_input_path = os.path.join(pt.data_dir, "parameters.yaml")

    def create_dict_from_yaml(self) -> dict[str, dict[str, dict[str, str]]]:
        with open(self.param_input_path, "r") as f:
            yaml_string = f.read()
        return yaml.safe_load(yaml_string)

    def build_substance_params(
            self,
            all_param_dict: dict[str, dict[str, dict[str, str]]]
    ):
        parameter_dict_list: list[dict[str, dict[str, str]]] = []
        parameter_class_list: list[SubstanceParameter]
        for parameter in all_param_dict.values():
            parameter_dict_list.append(parameter)
            print(parameter_dict_list)
        # for parameter_dict in parameter_dict_list:
        #     parameter = SubstanceParameter(
        #         name=parameter_dict.keys(),
        #         data=parameter_dict.values()
        #     )










def main():
    ph = ParamHandler()
    ph.build_substance_params(ph.create_dict_from_yaml())

if __name__ == "__main__":
    main()