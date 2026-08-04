from ..base import SecurityCheck
from ..registry  import CheckRegistry
from typing import Any , Dict
from pathlib import Path


@CheckRegistry.register
class MagicBytesCheck(SecurityCheck):
    
    """Since we can still have new filetype to check 
    we have decided to user simple registry under magic to allow the extensibility of the system
    does registry pattern is gonna be used here!! """
    
    #registry 
    _checkers = {}
    """It's class variable cs it will be shared across MagicBytes instances
    This means :
    all checkers are stored in one place
    you can add new checkers without creating an instance
    the registry persists accross the entire system 
    In addition its protected !! which mean it has to be used internally in this class"""
    def __init__(self, config:Dict):
        super().__init__(config)
        self.name = "MagicBytesCheck"
    @classmethod
    def register_format(cls, extension: str, checker_func):
        """Register a new checker function for a file extension 
        this is the Extension point for adding new formats
        args :
        extension: The file extension (e.g., '.json', '.csv')
        checker_func: A function that takes a Path and return bool"""
        cls._checkers[extension.lower()] = checker_func
    def get_config(self, key:str, default: Any =None) -> Any:
        """get configuration for this check."""
        return self.config.get('content_validation', {}).get(key, default)
    def check_file(self, filepath: Path) -> bool:
        """Verify that the file content matches its extension"""
        #getting file extension
        extension=filepath.suffix.lower()
        #checking whetaher the content validation is enabled in config
        content_validation=self.get_config('enabled', False)
        if not content_validation:
            return True
        #look up the checker function
        checker = self._checkers.get(extension)
        if not checker:
            return True
        return checker(filepath)
    def check_data(self, data : Any, format: str ='json') -> bool:
        return True
    @staticmethod
    def _check_json(filepath: Path) -> bool:
        try :
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content=f.read(100)
                stripped=content.lstrip()
                if not stripped:
                    return False
                if stripped[0] in '{[':
                    return True
                return False
        except Exception:
            return False
    @staticmethod    
    def _check_csv(filepath: Path) -> bool:
        try :
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines =[]
                for i in range(5):
                    line=f.readline()
                    if not line:
                        break
                    lines.append(line.strip())
                if not lines:
                    return False
                has_delimeter = any(
                    ',' in line or '\t' in line or ';' in line 
                    for line in lines
                )  
                if has_delimeter:
                    for line in lines:
                        parts=line.split(',')
                        if len(parts) < 2:
                            return False
                        
                    return True
        except Exception:
            return False
    @staticmethod    
    def _check_parquet(filepath: Path) ->bool:
        try:
            with open(filepath, 'rb') as f:
                magic=f.read(4)
                return magic == b'PAR1'
        except Exception:
            return False
    @staticmethod    
    def _check_xml(filepath: Path) -> bool:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content=f.read(100)
                stripped=content.lstrip()
                if not stripped:
                    return False
                if stripped.startswith('<?xml') or stripped.startswith('<'):
                    return True
                return False
        except Exception:
            return False    
MagicBytesCheck.register_format('.json', MagicBytesCheck._check_json)
MagicBytesCheck.register_format('.csv', MagicBytesCheck._check_csv)
MagicBytesCheck.register_format('.xml', MagicBytesCheck._check_xml)
MagicBytesCheck.register_format('.parquet', MagicBytesCheck._check_parquet)
            
          