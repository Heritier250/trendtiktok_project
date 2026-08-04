from typing import Any, Dict, List
from ..base import SecurityCheck
from pathlib import Path
from ..registry import CheckRegistry
import re

@CheckRegistry.register
class DangerousKeyCheck(SecurityCheck):
    def __init__(self, config:Dict):
        super.__init__(config)
        self.name = DangerousKeyCheck
    def get_config(self, key:str, default:Any=None):
        return self.config.get('content_validation', {}).get(key, default)
    def check_file(self, filepath:Path=None):
        """Since Dangerouskeycheck does not care about the file we have to return true"""
        return True
    def check_data(self, data:Any, format:str="json") ->bool:
        """This is where the real action gonna take place!!!"""
        rules=self._get_rules_for_format(format)
        if not rules:
            return True
        if self._scan_recursive(data, rules):
            self._log_attempts(format)
            return False
        return True
    def _get_rules_for_format(self, format:str) ->Dict:
        format_rules=self.get_config(format, {})
        if not format_rules:
            return {}
        return format_rules
    def _scan_recursive(self, obj: Any, rules:Dict) ->bool:
        """recursive scan for dangerous patterns using Duck typing
        this method check behavoir bot type!!
        isinstance is very dangerous here cs it might lead to 
        bypassing the scanner"""
        patterns= []
        for rule_type, rule_values in rules.items():
            if isinstance(rule_values, list):
                patterns.extend(rule_values)
            else:
                patterns.append(rule_values)
        if not patterns:
            return False
        if hasattr(obj, 'items') and callable(obj.items):
            for key, value in obj.items():
                if self._matches_patterns(key, patterns):
                    return True
                if self._scan_recursive(value, rules):
                    return True
                return False
            #if it behaves  like list but not string
        if hasattr(obj, '__iter__') and not hasattr(obj, '__str__'):
            for item in obj:
                if self._scan_recursive(item, rules):
                    return True
                return False
            #if it behaves like a string 
        if hasattr(obj, '__str__'):
            if self._matches_patterns(str(obj), patterns):
                return True
            return False
        #Fallback to unkown type! convert to string and scan
        if self._matches_patterns(str(obj), patterns):
            return True
        return False
    def _matches_patterns(self, value: str, patterns:List[str]) -> bool:
        """Check if a string matches any of the dangerous patterns
        supports:
        -Exact match: value == patterns
        -Contains match: pattern in value
        -Regex match: pattern.startswith('^')"""
        
        for pattern in patterns:
            if value == pattern:
                return True
            if pattern in value:
                return True
            if isinstance(pattern, str) and pattern.startswith('^'):
                if re.search(pattern, value):
                    return True
        return False
    def _log_attempts(self, format: str) -> None:
        from src.utils.logger import get_logger
        logger =get_logger("dangerous_keys")
        logger.critical(f"Damgerous content detected in {format} format")
        logger.critical(f"possible attack: prototype pollution, formula injection or xss")
        logger.critical("data rejected.security team alertd")          
                            
    
    
        
        
        
    
        