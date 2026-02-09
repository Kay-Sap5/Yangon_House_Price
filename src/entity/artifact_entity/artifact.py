import os
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    raw_dataset_file_path : str

@dataclass
class DataPreprocessingArtifact:
    train_data_file_path : str
    test_data_file_path : str

@dataclass
class DataValidationArtifact:
    valid_train_file_path : str
    valid_test_file_path : str

@dataclass
class DataFeatureEngineeringArtifact:
    feature_engineering_train_file_path : str
    feature_engineering_test_file_path : str

@dataclass
class DataTransformationArtifact:
    transformed_train_data_file_path : str
    transformed_test_data_file_path : str
    transformed_preprocessor_file_path : str

@dataclass
class ModelEvaluationMetricsArtifact:
    r2_score : float
    mean_absolute_error : float
    mean_square_error : float
    root_mean_square_error : float
    mean_absolute_percentage_error : float

@dataclass
class ModelTrainingArtifact:
    trained_final_model_file_path : str
    train_model_evaluation : ModelEvaluationMetricsArtifact
    test_model_evaluation : ModelEvaluationMetricsArtifact



