import os
import sys

from src.logging.logger import logging
from src.exception.exception import CustomException

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    GradientBoostingRegressor)

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
models = {'LinearRegression':LinearRegression(),
          'SVR':SVR(),
          'DecisionTreeRegressor':DecisionTreeRegressor(),
          'XGBRegressor':XGBRegressor(),
          'RandomForestRegressor':RandomForestRegressor(),
          "AdaBoostRegressor":AdaBoostRegressor(),
          'GradientBoostingRegressor':GradientBoostingRegressor()}
# models = {
        #   'RandomForestRegressor':RandomForestRegressor(),
        #   'GradientBoostingRegressor':GradientBoostingRegressor()}
param_grids = {
    'LinearRegression': {
        'fit_intercept': [True, False],
        'positive': [True, False]
    },
    'SVR': {
        'C': [0.1, 1, 10, 100],
        'epsilon': [0.01, 0.1, 0.5],
        'kernel': ['rbf', 'poly', 'sigmoid'],
        'gamma': ['scale', 'auto']
    },
    'DecisionTreeRegressor': {
        'max_depth': [None, 5, 15, 30],
        'min_samples_split': [2, 10, 20],
        'min_samples_leaf': [1, 5, 10],
        'max_features': [None, 'sqrt', 'log2']
    },
    'XGBRegressor': {
        'n_estimators': [100, 500, 1000],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 7, 10],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'gamma': [0, 0.25, 0.5]
    },
    'RandomForestRegressor': {
        'n_estimators': [100, 300, 600],
        'max_depth': [10, 30, None],
        'min_samples_split': [2, 5, 15],
        'min_samples_leaf': [1, 2, 8],
        'max_features': ['sqrt', 'log2'],
        'bootstrap': [True, False]
    },
    'AdaBoostRegressor': {
        'n_estimators': [50, 150, 300],
        'learning_rate': [0.001, 0.01, 0.1, 1.0],
        'loss': ['linear', 'square', 'exponential']
    },
    'GradientBoostingRegressor': {
        'n_estimators': [100, 400, 800],
        'learning_rate': [0.01, 0.1],
        'subsample': [0.7, 0.9, 1.0],
        'max_depth': [3, 6, 12],
        'min_samples_leaf': [1, 4, 9],
        'loss': ['squared_error', 'huber']
    }
}
# param_grids = {
    
#     'RandomForestRegressor': {
#         'n_estimators': [10,20],
#         'max_depth': [10, None],
#         'min_samples_split': [2, 15],
#         'min_samples_leaf': [1, 8],
#         'max_features': ['log2'],
#         'bootstrap': [ False]},

#     'GradientBoostingRegressor': {
#         'n_estimators': [10, 20],
#         'learning_rate': [0.01, 0.1],
#         'subsample': [0.7, 0.9, 1.0],
#         'max_depth': [3, 6, 12],
#         'min_samples_leaf': [1, 4, 9],
#         'loss': ['squared_error']
#     }
# }



def model_trainer(x_train , y_train , x_test , y_test , models , params) -> dict:
    logging.info("Entered model_trainer method")
    try:
        r2 = {}
        for i in range (len(list(models.keys()))):
            model = list(models.values())[i]
            model_name = list(models.keys())[i]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(
                estimator=model,
                param_grid=param,
                cv=3,
                n_jobs=-1,
                verbose=1
            )
            gs.fit(X=x_train,y=y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(x_train , y_train)

            y_pred = model.predict(x_test)
            score = r2_score(y_test , y_pred)

            r2.update({model_name : score})
        return r2
    except Exception as e:
        raise CustomException(e,sys)
    


class NetworkModel:
    def __init__(self , model , preprocessor):
        logging.info("Entered NetworkModel Object")
        try:
            self.model = model
            self.preprocessor = preprocessor        
        except Exception as e:
            raise CustomException(e,sys)
        
    def predict(self,x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transformed)

            return y_pred
        except Exception as e:
            raise CustomException(e,sys)
