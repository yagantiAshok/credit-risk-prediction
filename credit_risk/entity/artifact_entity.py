

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

