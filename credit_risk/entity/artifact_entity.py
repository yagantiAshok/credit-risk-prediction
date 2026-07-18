

from dataclasses import dataclass
@dataclass
class dataingestionartifact:
    train_filepath:str
    validation_filepath:str
@dataclass
class DatavalidationArtifcat:
    validation_status:bool
    drift_filepath:str
    data_drift_status:bool
@dataclass
class DataTransformationArtifact:
    processed_train_filepath:str
    processed_validation_filepath:str
    processed_obj_filepath:str
@dataclass
class ModelTrainingArtifcat:
    trained_model:object
    f1_score:float
    recall:float
    accuracy:float
    precision:float