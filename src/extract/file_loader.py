import json
import  re
from datetime import datetime
from pathlib import Path
from src.utils.logger import get_logger 
from src.extract.cached import Serializer, PathBuilder
from typing import Dict, List, Union, Optional, Any
from abc import ABC , abstractmethod
import pandas as pd
from src.utils.config_loader import load_file_config
import xml.etree.ElementTree as ET 

logger=get_logger('file_loader')

class DataLoader(ABC):
    #Each kind of file should implement this method no matter what!!!!!!
    @abstractmethod
    def load(self, filename:str)->Optional[Union[List, Dict]]:
        """Loading data from file"""
    
class InterfaceValidator(ABC):
    @abstractmethod
    def validating_file_size(self, filepath:Path):
        """will be validating file  size"""
    @abstractmethod
    def validating_file_existance(self, filepath:Path):
        """checking whether the file is exist"""
    @abstractmethod
    def validating_format(self, filename):
        """shecking whether the format is allowed"""
    @abstractmethod
    def validating_file_enabled(self, file_type):
        """checking whether the extracted file is available"""
    @abstractmethod
    def validating_field_required(self, data:Dict, file_type):
        """checking whether the file has the required fields"""    
class Validator(InterfaceValidator):
    
    def __init__(self, config:Dict=None):
        if config is None:
            config=load_file_config()
        self.config=config
        logger.info("Validator initailized")   
        """Setting up the helper function to eradicate the Violation of DRY principle!!
        1.starting with extracting the confifugaration's specifications"""
        #helperf unction _get_validation
    def _get_validation(self):
        return self.config.get('validation', {})  
        #helper function _get_schema
    def _get_schema(self):
        return self.config.get('schema', {})   
       #helper function _get_format
    def _get_format(self):
        return self.config.get('formats', {})   
    def validating_file_existance(self, filepath:Path)->bool:
        if not filepath.exists():
            logger.warning(f"{filepath} does not exist")
            return False
        return True
    
    def validating_file_size(self, filepath:Path)->bool:
        validation_config=self._get_validation()
        file_sizemb=validation_config.get('max_file_size_mb', 100)
        file_sizekb=validation_config.get('min_file_size_kb', 1)
        
        file_size=filepath.stat().st_size 
        
        filesize_in_kb=file_size / 1024
        filesize_in_mb=file_size /(1024 * 1024)
        
        if filesize_in_kb < file_sizekb:
            logger.warning(f'{filepath} is too small, file seems to be empty!!')
            return False
        
        if filesize_in_mb > file_sizemb:
            logger.warning(f"{filepath} is to large to be loaded")
            return False
        return True
    def validating_format(self, filename):
        validation_config=self._get_validation()
        allowed_format=validation_config.get('allowed_extensions', ['json'])
        
        import os
        ext=os.path.splitext(filename)[1].lower()
        if ext not in allowed_format:
            logger.warning(f"{ext} is not allowed!! , what llow are {allowed_format}")
            return False
        return True
    def validating_file_enabled(self, file_type):
        formats=self._get_format()
    
        format_config=formats.get(file_type.lower(),{})
        enabled=format_config.get('enabled', False)
        if not enabled:
            logger.warning(f" the {file_type} file is disabled")
            return False
        return True
    def validating_field_required(self, data:Any):
        fields=self._get_schema()
        file_field=fields.get('required_fields', [])
        if not file_field:
            return True
        sample=None
        if hasattr(data, '__getitem__') and hasattr(data, '__len__'):
            if len(data) > 0:
                sample=data[0]
            else:
                logger.warning("There is no required data in given data")
                return True
        elif hasattr(data, 'get'):
            sample=data
        else:
            logger.warning(f"data does not support indexing of get{type(sample)}")
            return False
        if not hasattr(sample, 'keys'):
            logger.warning(f"sample does not have  key method {type(sample)}")
            return False
        available_fields=list(sample.keys())
        missing_fields=[]
        type_error=[]
        for field in file_field:
            field_name=field.get('name')
            field_type=field.get('type')
            required=field.get('required', True)
            if field_name not in sample:
                if required:
                    missing_fields.append(field_name)
                continue
            value=sample[field_name]
            if field_type == "string":
                if not hasattr(value, "__str__"):
                    type_error.append(f"{field_name} cannot be converted to string!!!")
            elif field_type =="integer":
               if not hasattr(value, "__int__"):
                    type_error.append(f"{field_name} cannot be used as string please")
            elif field_type == "float":
                if not hasattr(value, "__float__"):
                    type_error.append(f"{field_name} cannot be used as float")
            elif field_type == "number":
               if not hasattr(value, "__add__"):
                    type_error.append(f"{field_name} cannot be used as number")
            elif field_type == 'boolean':
               if not hasattr(value, "__bool__"):
                    type_error.append(f"{field_name} cannot be used as boolean")                                                 
            
        if missing_fields:
            logger.warning(f"missing fields are  : {missing_fields}")
            logger.warning(f"availabe fields : {available_fields}")
            return False 
        
        logger.info(f"all required fields present :{self.file_field}")
        return True
    def validating_all(self, filename, file_type, data: Any, filepath:Path) -> bool:
        checks=[
            
            self.validating_file_existance(filepath),
            self.validating_file_enabled(file_type),
            self.validating_format(filename),
            self.validating_file_size(filepath),
            self.validating_field_required(data, file_type),
            
            
        ]     
        return all(checks)

class JSONLOADER(DataLoader):
    def load(self, filename:Path):  
        if Validator.validating_file_existance(filename):
            try :
                with open(filename, "r", encoding="utf-8") as f:
                    return json.loads(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}
        else:
            raise FileNotFoundError (f"File does not exist ") 
class CSVLoader(DataLoader):
    pass        
