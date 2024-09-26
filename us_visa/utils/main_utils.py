import os
import sys
import numpy as np
import dill
import yaml
from pandas import DataFrame
from us_visa.exception import USvisaException
from us_visa.logger import logging

def read_yaml_file(file_path: str):
    """
    Reads a YAML file and returns its content.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The content of the YAML file as a dictionary.

    Raises:
        USvisaException: If there is an error in reading the YAML file.
    """
    try:
        with open(file=file_path, mode="rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise USvisaException(e, sys) from e

def write_yaml_file(file_path: str, content: dict, replace: bool = False):
    """
    Writes content to a YAML file. If replace is True, it will remove the
    existing file before writing.

    Args:
        file_path (str): The path to the YAML file.
        content (dict): The content to write to the file.
        replace (bool): If True, replace the existing file.

    Raises:
        USvisaException: If there is an error in writing the YAML file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file=file_path, mode='w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise USvisaException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves a NumPy array to a binary file.

    Args:
        file_path (str): The path to save the NumPy array.
        array (np.array): The NumPy array to save.

    Raises:
        USvisaException: If there is an error in saving the NumPy array.
    """
    try:
        dir_path = os.path.dirname(file_path)
        # Create the directory if it does not exist
        os.makedirs(dir_path, exist_ok=True)
        with open(file=file_path, mode="wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise USvisaException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads a NumPy array from a binary file.

    Args:
        file_path (str): The path to the NumPy array file.

    Returns:
        np.array: The loaded NumPy array.

    Raises:
        USvisaException: If there is an error in loading the NumPy array.
    """
    try:
        with open(file=file_path, mode='rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise USvisaException(e, sys) from e

def load_object(file_path: str):
    """
    Loads a Python object from a binary file using dill.

    Args:
        file_path (str): The path to the file containing the object.

    Returns:
        object: The loaded Python object.

    Raises:
        USvisaException: If there is an error in loading the object.
    """
    logging.info("Entered the load_object method of utils")
    try:
        with open(file=file_path, mode='rb') as file_obj:
            obj = dill.load(file_obj)

        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise USvisaException(e, sys) from e

def save_object(file_path: str, obj: object):
    """
    Saves a Python object to a binary file using dill.

    Args:
        file_path (str): The path to save the object.
        obj (object): The Python object to save.

    Raises:
        USvisaException: If there is an error in saving the object.
    """
    logging.info("Entered the save_object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file=file_path, mode='wb') as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")
        return obj
    except Exception as e:
        raise USvisaException(e, sys) from e

def drop_columns(df: DataFrame, cols):
    """
    Drops specified columns from a DataFrame.

    Args:
        df (DataFrame): The DataFrame from which to drop columns.
        cols (list): The list of column names to drop.

    Returns:
        DataFrame: The DataFrame after dropping the specified columns.

    Raises:
        USvisaException: If there is an error in dropping columns.
    """
    logging.info("Entered the drop_columns method of utils")
    try:
        df = df.drop(columns=cols, axis=1)
        logging.info("Exited the drop_columns method of utils")
        return df
    except Exception as e:
        raise USvisaException(e, sys) from e
