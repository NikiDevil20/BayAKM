from pathlib import Path
import os

class DirPaths:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent.absolute()


        self.src_dir = os.path.join(self.base_dir, "src")
        self.docs_dir = os.path.join(self.base_dir, "docs")
        self.tests_dir = os.path.join(self.base_dir, "tests")
        self.data_dir = os.path.join(self.src_dir, "data")

        self.main_dir = os.path.join(self.src_dir, "bayakm")


def main():
    pt = DirPaths()
    print(pt.base_dir, pt.src_dir, pt.docs_dir)

if __name__ == "__main__":
    main()