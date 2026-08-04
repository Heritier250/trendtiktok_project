from typing import List, Dict, Any
from ..base import SecurityCheck
from ..registry import CheckRegistry
from pathlib import Path

@CheckRegistry.register
class SizeCheck(SecurityCheck):
    """validate file size 
    checks:
    -Minimum size (min_file_size_kb)
    -Maxim size (max_file_size_mb)
    Prevents:
    -Empty or corrupted files (too small)
    -DoS attacks (too large)"""
    
    def __init__(self,  config: Dict):
        super().__init__(config)
        self.name = "SizeCheck"
        self._load_limits()
    def _load_limits(self) -> None:
        validation=self.config.get('validation', {})
        self.max_size_mb = validation.get('max_file_size_mb', 100)
        self.min_size_kb = validation.get('min_file_size_kb', 1)
    def check_file(self, filepath: Path) -> bool:
        size_bytes = filepath.stat().st_size
        size_kb = size_bytes / 1024
        size_mb = size_bytes / (1024 * 1024)
        
        
        if size_kb < self.min_size_kb:
            return False
        
        if size_mb > self.max_size_mb:
            return False
        return True
    def check_data(self, data: Any, format: str = "json") -> bool:
        """This check doesn't care about data"""
        return True      
     
     
    


