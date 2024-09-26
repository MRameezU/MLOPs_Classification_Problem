import os
import sys

import numpy as np
import dill
import yaml
from pandas import DataFrame

from us_visa.exception import USvisaException
from us_visa.logger import logging

def read_yaml_fiel(file_path:str):
    try:
        with open(file=file_path,mode="rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise USvisaException(e,sys) from e

def write_yaml_file(file_path,content,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            with open(file=file_path,mode='w') as file:
                yaml.dump(content,file)
    except Exception as e:
        raise USvisaException(e,sys) from e

def load_object(file_path):
    ...