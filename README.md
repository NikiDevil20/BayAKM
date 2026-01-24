# BayAKM

## :information_source: General information

This script utilizes [bayesian optimization](https://b-shields.github.io/publication/2021-02-03-Nature-7) to find the optimal reaction conditions from a set of parametersand is based on the python package [BayBE](https://emdgroup.github.io/baybe/stable/index.html) by Merck.
Parameters can either be numeric (concentration, temperature etc.) or substances (base, ligand, solvent etc.). If substance parameters are chosen, their chemical properties are accounted for via chemical encoding (e.g. [MORDRED](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-018-0258-y) encoder).
The script then recommends parameters for the next reactions in the results file.

[Bayesian optimization explanation by baybe developer Martin Fitzner from Merck](https://www.youtube.com/watch?v=OKHcwtefRsU)

## :bulb: Features

### :test_tube: Implemented

- SearchSpaces of discrete Parameters
  - NumericalParameters
  - SubstanceParameters
- Different AcquisitionFunctions
- Exclude combinations via constraints
- SHAP insights

### :construction: Planned

- Probability of Improvement (PI) based early stopping

## :gear: Installation

1. Download the repository as a ZIP file and extract it.
2. Install [Python 3.13](https://www.python.org/downloads/) and when asked, add to PATH
3. 

## :scroll: Getting your recommendation

1. Run the `bayakm.bat` file.
2. Click "New Campaign" and enter the required information.
3. Add at least two parameters with at least two values.
4. (Optional) Add constraints to exclude certain combinations.
5. Click "Get first Recommendation!"
6. Note the recommended conditions and run the experiments. The application may be closed.
7. Reopen the application and enter the yields.
8. Click on "Save" and "New Recommendation" to proceed with the campaign.




