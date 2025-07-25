import os
from pathlib import Path


class DirPaths:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent.absolute()

        self.bayakm_dir = os.path.join(self.base_dir, "bayakm")

        self.src_dir = os.path.join(self.bayakm_dir, "src")
        self.docs_dir = os.path.join(self.base_dir, "docs")
        self.tests_dir = os.path.join(self.base_dir, "tests")
        self.data_dir = os.path.join(self.bayakm_dir, "data")

        self.config_path = os.path.join(self.data_dir, "config.yaml")
        self.output_path = os.path.join(self.data_dir, "results.csv")

def main():
    pt = DirPaths()
    print(pt.base_dir, pt.src_dir, pt.docs_dir)

if __name__ == "__main__":
    main()