# 04 - NEST, a Data-driven Building Model
## Summary
Predictive building modelling to improve building operation.

## The Goal
Energy consumption and CO2 emmissions of buildings could be reduced significantly by improving the controlling of the heating and cooling systems. This must be done predictively due to the thermal inertia. Hence, the control requires an accurate prediction model.

## The Challenge
The Empa team proposed this challenge (https://hack.opendata.ch/project/672) for the ENERGY &amp; CLIMATE HACK 2021. Starting point was a research project on data predictive control. The proposed challenge was to improve the statistical modelling of the correlations between building controls and resulting room temperatures.

We have picked the data set for the SolAce unit (https://info.nestcollaboration.ch/wikipediapublic/building/solace/)

## The Idea
We train a machine-learning algorithm to maintain a target temperature. The system is set up as two stages:
1. Feature selection using the SULOV algorithm in Featurewiz.
2. Use genetic programming in TPOT to automatically explore thousands of models.

### Featurewiz
Select the model features. We use Featurewiz (an open-source python package) for automatically creating and selecting important features in the dataset that will create the best model with higher performance. Featurewiz uses the SULOV algorithm and Recursive XGBoost to reduce features to select the best features for the model. It also allows us to use advanced feature engineering strategies to create new features. 

Featurewiz uses the SULOV (Searching for Uncorrelated List of Variables) algorithm. The algorithm works in the following steps.
1. First step: find all the pairs of highly correlated variables exceeding a correlation threshold (say absolute(0.8)).
2. Second step: find their Mutual Information Score to the target variable. Mutual Information Score is a non-parametric scoring method. So it's suitable for all kinds of variables and target.
3. Third step: take each pair of correlated variables, then knock off the one with the lower Mutual Information Score.
4. Final step: Collect the ones with the highest Information scores and least correlation with each other.

### TPOT
We use the TPOT (Tree-based Pipeline Optimization Tool) Python library for automated machine learning. TPOT uses a tree-based structure to represent a model pipeline for a predictive modeling problem, including data preparation and modeling algorithms, and model hyperparameters.

TPOT optimizes machine learning pipelines using genetic programming. It explores thousands of possible pipelines to find the best one for the data. Once TPOT is finished searching, it provides Pythons code for the best pipeline it found so we can tinker with the pipeline from there.

## What we did
The model was trained using Jupyter notebooks on Google Collab on a subset of the data in order to get results in a reasonable time.

## The prototype
Featurewiz selected 11 optimal features:
![Title](https://github.com/WolframWilluhn/ENRGCLIM21_04_NEST/blob/main/Modelling/Sampled_fulldata_extended.png)

TPOT chose the XGBRegressor moddel as the best pipeline.

## Resources/ Data
We have been using the SolAce Energy Demand and User Behaviour Data (https://figshare.com/articles/dataset/NEST_-_SolAce_Energy_Demand_and_User_Behaviour_Data/14376950). It contains 18 measurement points with a temporal resolution of 1 minute over the period of one year (July 2019 to July 2020).

The room temperature is a result of heat inflows and outflows of the unit.
Heat inflows are
- Space heating delivered to the unit.
- Radiation that is coming through the windows.
- Heat generated by the people present in the room.
Heat outflows are
- Heat that is transfered through the walls and windows to the outside world.
- Space cooling delivered to the unit.

There are energy meters for the space heating and cooling delivered to the unit. We engineered the following features:
- temp_room = average of temp_meeting and temp_office
- rad_room = irrad * (blinds_height_F1 + blinds_height_F2 + blinds_height_F3 + blinds_height_F4) during 11am and 5pm and 0 outside of these hours
- praes_room = maximum of praes_meeting and praes_office
- temp_diff = temp_amb - temp_room

In addition, we have added the following time-based variables to help the algorithm deal with time-dependent phenomena:
- day_of_week = 0 for Monday to 6 for Sunday
- is_weekend = true for Saturday and Sunday
- hour = hour of time variable

## Next Steps
The is a number of next steps that should be taken from here
- Due to time constraints, the current models were created with only a subset of the available data. With more time available, the training should be re-run with the entire data sets or with even larger data sets containing multiple years.
- Specially constructured additional features can often improve a models performance. A few features have been created as part of this project. A possible next step should explore even more features.
- In addition to the statistical analysis, the same data could be further analyzed through visualization. In particular, it would be interesting to investigate the temporal delays of the change in indoor temperature caused by energy input subject to the thermal inertia. The challenge submission suggested to look at H-scatterplots and cross-correlograms as tools to understand lagged correlations.
- Finally, in order to establish trust in the results of the statistical model, model predictions should be validated through various analyses. The visualizations from the previous step could be adequate tools in order to understand how the predictions differ from actual measurements and, more importantly, how novel control algorithms reduce energy consumption while maintaining the same level of comfort.
