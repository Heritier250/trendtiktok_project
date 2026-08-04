from typing import Any, Dict, List
from pathlib import Path
from ..base import SecurityCheck
from ..registry import CheckRegistry
import re


@CheckRegistry.register
class SensitiveDataCheck(SecurityCheck):
    """it's main job is just to scan for sensitive pattern"""
    def __init__(self, config: Dict):
        super().__init__(config)
        self.name = "SensitiveDataCheck"
    def get_config(self, key :str, default: Any = None) ->Any:
        return self.config.get('sensitive_data', {}).get(key, default)
    def check_file(self, filepath:Path):
        """This check does not care about the file"""
        return True   
    def check_data(self, data:Any, format:str ='json') ->bool:
        """Scan data for sensitive patterns"""
        if not self.get_config('enbled', True):
            return True
        patterns = self._get_patterns()
        if not patterns:
            return True
        if self._scan_recursive(data, patterns):
            self._log_attemps(format)
            return False
        return True
    def _get_patterns(self) -> List[Dict]:
        """load patterns from configuration file"""
        return self.get_config('patterns, []')
    def _scan_recursive(self, obj:Any, patterns:List[Dict]) ->bool:
        """Recursively scan for sensitive patterns using duck typing""" 
        if hasattr(obj, '__str__'):
            if self._check_string(str(obj), patterns):
                return True
        if hasattr(obj, 'items') and callable(obj.items):
            for value in obj.values():
                if self._scan_recursive(value, patterns):
                    return True
        if hasattr(obj, '__iter__') and not isinstance(obj, str):
            for item in obj:
                if self._scan_recursive(item, patterns):
                    return True
        return False
    def _check_string(self, value: str, patterns: List[Dict]) -> bool:
        for pattern_info in patterns:
            pattern=pattern_info.get('pattern', '')
            if pattern and re.search(pattern, value):
                return True
            return False
    def _log_attemps(self, format:str)->None:
        from src.utils.logger import get_logger
        logger=get_logger('sensitive_data')
        logger.critical(f'SENSITVE DATA DETECTED in  {format} format')
        logger.critical("possible data leak")
        logger.critical('data rejected')   
                    