from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path: str  # Path to the training dataset file
    test_file_path: str   # Path to the testing dataset file


@dataclass
class DataValidationArtifact:
    validation_status:bool
    message:str
    drift_report_file_path:str