from abc import ABC , abstractmethod
from typing import Dict, Any
from pathlib import Path

#This is an interface that will be used throughout checks
class SecurityCheck(ABC):
    def __init__(self,config:Dict):
        self.config= config
        self.name= self.__class__.__name__
    @abstractmethod    
    def check_file(self, filepath:Path) ->bool:
        """Override for the file level check
        default :pass (return True)
        THis will check:
        -Extensioncheck: ensure whether the file exetension is allowed
        -Magicbytechecks: ensure that the file content is not harmful
        -Sizecheck: ensure that the file size is meeting with prescribed one in configurations"""
        pass
    

     
    @abstractmethod
    def check_data(self, data: Any) -> bool:
        """Override for the data_level check
        NB it must be implemented by all checks 
        include dangerous_key: check for __proto__, _constractor
        , sensitivedata : looking for PII, 
        schema_check: checking the existance of required fields, size"""
        pass
    @abstractmethod
    def get_config(self, key: str, default: Any=None) -> Any:
        """Each checkfile you should implement  get_config() privately  """
        pass
        
            