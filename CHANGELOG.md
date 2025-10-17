# Changelog

All notable changes to this project will be documented in this file.



## [0.2.1] - 2025-10-17

### Fixed
- When removing rows while creating substance parameters, the entires where only removed from the gui, but not from the file.
- Now uses Farthest Point Search for initial recommendation in discrete searchspaces
- An error window is opened if a parameter name is already in use instead of passing silently



## [0.2.0] - 2025-10-04

### Added
- Entires in the recommendation table now get checked against the allowed values

### Fixed
- Insight frame raises Error if opened without measurements in campaign.
- Two parameters can no longer have duplicate values
- Parameter displays now get drawn from campaign object instead of creating a list from the parameters.yaml file



## [0.1.0] - 2025-09-27

### Added
- Full functionality for creating campaigns, adding measurements and getting new recommendations with Substance, Numerical Discrete and Continuous Parameters.


