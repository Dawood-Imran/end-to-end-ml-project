import pandas as pd
import os
import sys

from dataclasses import dataclass


from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
#from xgboost import XGBRegressor
# from catboost import CatBoostRegressor
from sklearn.metrics import  r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_model





@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', 'model.pkl')


class ModelTrainer:
    def __init__(self) -> None:
        # This variable will contain the file path for the trained model
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                #"XGBoost": XGBRegressor(),
                #"CatBoost": CatBoostRegressor(verbose=False),
                "AdaBoost": AdaBoostRegressor(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Linear Regressor": LinearRegression(),
            }

            param_grid = {
                "Random Forest": {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [None, 10, 20, 30],
                    #'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                    #'bootstrap': [True, False]
                },
                "Decision Tree": {
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    #'min_samples_leaf': [1, 2, 4],
                    #'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
                },
                "Gradient Boosting": {
                    #'n_estimators': [100, 200, 300],
                    'learning_rate': [0.01, 0.1, 0.05],
                    'max_depth': [3, 5, 10],
                    'min_samples_split': [2, 5, 10],
                    #'min_samples_leaf': [1, 2, 4]
                },
                "AdaBoost": {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.5, 1.0],
                    #'loss': ['linear', 'square', 'exponential']
                },
                "K-Neighbors Regressor": {
                    'n_neighbors': [3, 5, 10],
                    #'weights': ['uniform', 'distance'],
                    #'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                    'leaf_size': [10, 30, 50]
                },
                "Linear Regressor": {
                    #'fit_intercept': [True, False],
                    #'normalize': [True, False],
                    #'copy_X': [True, False]
                }   
            }


            model_report:dict = evaluate_model(X_train,X_test,y_train,y_test,models = models,param = param_grid)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")

            logging.info(f"Best model is {best_model_name} with a score of {best_model_score}")

            # creating the pickle file for the model
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)

            return r2_square

            
        except Exception as e:
            raise CustomException(e,sys)







    








