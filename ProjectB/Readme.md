### Weather Forecasting Project

Lea Frost

For CSCE 580 - Artificial Intelligence


Summary:
This project explores multivariate weather forecasting using various models.
The most diffficult part was data preprocessing since most models do not
inherently understand continuous time relationships. I cyclically encoded 
time using sine/cosine transformations so the models view time as a cycle
rather than as a linear variable. 


I first explored regression tasks, specifically focusing on temperature but
can easily be used to predict other variables. 

I then explored classification tasks, specifically predicting the presence of 
rain which is a notoriously difficult task. 

Structure:
- Regression (temperature)
    - ./Hourly/Temperature/
        - linear_reg.ipynb
        - random_forest.ipynb
        - SVR.ipynb
- Classification (rain or no rain)
    - ./Hourly/Rain Class/
        - logistic_reg.ipynb
        - random_forest_class.ipynb
        - xgboost.ipynb



