LINK_SCRAPPER_SAVED_LINK_FILE_PATH : str = "src/update_database/Saved_Links/links.csv"

DATABASE_NAME = 'House_Price_Shwe_Property'
COLLECTION_NAME = 'raw_scraped_data'

TRAIN_TEST_SPLIT_RATIO = 0.2

# Artifact Folder
ARTIFACT_DIR_NAME = 'Artifacts'

# Data Ingestion
DATA_INGESTION_DIR_NAME = 'data_ingestion'
DATA_INGESTION_INGESED_DIR_NAME = 'ingested'
DATA_INGESTION_DATASET_FILE_NAME = 'raw_dataset.csv'

# Data Preprocessing
DATA_PREPROCESSING_DIR_NAME = 'data_preprocessing'
DATA_PREPROCESSING_fULL_DATA_DIR_NAME = 'full_data'
DATA_PREPROCESSING_fULL_DATA_NAME = 'full_data.csv'

DATA_PREPROCESSING_TRAIN_AND_TEST_DIR_NAME = 'train_and_test'
TRAIN_DATA_NAME = 'train.csv'
TEST_DATA_NAME = 'test.csv'

TARGET_NAME = 'price'

# Data Validation
DATA_VALIDATION_DIR_NAME = 'data_validation'
DATA_VALIDATION_VALID_DIR_NAME = 'valid'
DATA_VALIDATION_INVALID_DIR_NAME = 'invalid'

DATA_SCHEMA_YAML_FILE_PATH = 'data_schema/schema.yaml'

# Data Feature Engineeing
FEATURE_ENGINEERING_DIR_NAME = 'feature_engineering'
FEATURE_ENGINEERING_APPLIED_DATA_DIR = 'applied'
FEATURE_ENGINEERING_DATA_FEATURE_REPORT_DIR = 'data_feature_report'
FEATURE_ENGINEERING_DATA_FEATURE_REPORT_FILE_PATH = 'data_feature_report.yml'


# Data Transformation
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = 'transformed_data'
DATA_TRANSFORMATION_PREPROCESSOR_DIR_NAME = 'preprocessor'
DATA_TRANSFORMATION_PREPROCESSOR_FILE_NAME = 'preprocessor.pkl'

# Model Training
MODEL_TRAINING_DIR_NAME = 'model_training'
MODEL_TRAINING_TRAINED_MODEL_DIR_NAME = 'trained_model'
MODEL_TRAINING_TRAINED_MODEL_FILE_NAME = 'trained_model.pkl'
MODEL_TRAINING_PREPROCESSOR_DIR_NAME = 'preprocessor'
MODEL_TRAINING_PREPROCESSOR_FILE_NAME = 'preprocessor.pkl'
MODEL_TRAINING_FINAL_MODEL_DIR = 'final_model'
MODEL_TRAINING_FINAL_MODEL_FILE_NAME = 'final_model.pkl'







