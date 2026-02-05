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


