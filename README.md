# MLOPs_Classification_Problem

This repository contains an MLOps production-ready project designed to handle a classification problem using a dataset from Kaggle. The project integrates data ingestion, validation, transformation, model training, evaluation, and deployment components, following best practices in MLOps.

## Project Overview

The project aims to build an automated machine learning pipeline that efficiently manages the entire ML workflow, from data ingestion to model deployment. The project architecture is structured to ensure modularity, scalability, and ease of maintenance.

### Key Features

- **Automated ML pipeline**: Ingest, validate, transform data, train, evaluate, and deploy models automatically.
- **Modular design**: Each component of the pipeline is encapsulated for easy updates and maintenance.
- **Production-ready**: Configured to handle real-world data and deployment scenarios using industry-standard MLOps tools.

### Flowchart

A detailed flowchart of the project pipeline can be viewed [here](https://whimsical.com/).

### MLOps Tool

Evidently AI is used for monitoring model performance and data drift. Check it out [here](https://evidentlyai.com/).

### Dataset

The project uses the EasyVisa dataset, available on Kaggle: [EasyVisa Dataset](https://www.kaggle.com/datasets/moro23/easyvisa-dataset).

## Project Structure

The project follows a well-defined structure that separates different stages of the ML pipeline into distinct components. Below is an overview of the main directories and files in the project:

```
us_visa/
│
├── components/                 # Core components of the pipeline
│   ├── __init__.py
│   ├── data_ingestion.py       # Handles data collection from the source
│   ├── data_validation.py      # Ensures data quality and schema validation
│   ├── data_transformation.py  # Preprocessing and feature engineering
│   ├── model_trainer.py        # Model training logic
│   ├── model_evaluation.py     # Model evaluation metrics and analysis
│   └── model_pusher.py         # Deployment logic for pushing models to production
│
├── configuration/              # Configuration files for pipeline parameters
│   └── __init__.py
│
├── constants/                  # Project constants
│   └── __init__.py
│
├── entity/                     # Custom classes and data entities
│   ├── __init__.py
│   ├── config_entity.py
│   └── artificial_entity.py
│
├── exception/                  # Custom exception handling
│   └── __init__.py
│
├── logger/                     # Logging setup
│   └── __init__.py
│
├── pipeline/                   # Pipeline orchestration
│   ├── __init__.py
│   ├── training_pipeline.py    # Main training pipeline script
│   └── prediction_pipeline.py  # Pipeline for running predictions
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   └── main_utils.py
│
├── notebook/                   # Jupyter notebooks for experimentation
│   └── mongodb_demo.ipynb
│
├── app.py                      # Main application entry point
├── demo.py                     # Demo script showcasing the pipeline usage
├── requirements.txt            # List of dependencies
├── Dockerfile                  # Docker setup for containerization
├── setup.py                    # Project setup script
└── config/
    ├── model.yaml              # Model configuration parameters
    └── schema.yaml             # Schema definition for data validation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker (optional for containerization)
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/MLOPs_Classification_Problem.git
   cd MLOPs_Classification_Problem
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

To start the training pipeline, run:

```bash
python app.py
```

### Docker Setup

To run the project in a Docker container:

```bash
docker build -t mlops_classification .
docker run -p 8000:8000 mlops_classification
```

## Contributing

Feel free to contribute to this project by opening issues, suggesting new features, or submitting pull requests.

## Questions?

If you have any questions regarding this project, please reach out via the Issues section or contact the project maintainers.

---

This README provides a clear overview of the project, its structure, and instructions to get started. Let me know if you need further adjustments or additional sections!
