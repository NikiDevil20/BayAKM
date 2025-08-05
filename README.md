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
  - LogEI
  - PI
  - UCB
- Exclude combinations via constraints
- Tracking of PI for early campaign stopping

### :construction: Planned

- transfer learning
- continuous SearchSpaces

## :scroll: Getting your recommendation

1. Configure your settings in the `config.yaml` file.
2. Set up your parameters in the `parameters.yaml` file.
3. Execute the `main.py` file.
4. See your initial set of recommendations in the `results.csv` file.
5. Run the experiments, or choose other conditions. It's just a recommendation after all :upside_down_face:
6. Enter your measured results (and your reaction conditions, if you didn't choose the recommended) in the `results.csv` file.

    > :rotating_light: If you chose your own conditions make sure that all parameters are included in the parameters used to build the campaign. Otherwise an error will be raised. :rotating_light:

7. To run the optimiziation campaign, simply reapeat steps 3 - 6 until satisfied.

## :cd: Getting started

Downloads:

- [Python via anaconda distribution](https://www.anaconda.com/download/success)
- [Visual studio code](https://code.visualstudio.com/)
- `BayAKM folder` via github or sciebo

1. Open VS-Code
2. Open `BayAKM folder`
3. Open python Terminal
4. Enter `pip install baybe[chem,simulation,insights]`

## :bug: Help and Bugs

If you get stuck im happy to help you out :sunglasses:
Please report any bugs you find, so I can try to fix them