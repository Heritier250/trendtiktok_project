from typing import Any , Dict, Callable
from ..base import SecurityCheck
from ..registry import CheckRegistry
from pathlib import Path


@CheckRegistry.register
class StructureCheck(SecurityCheck):
    """Validate the structure of parsed data.
    uses an internal registry for format-specificcheckers
    such that  new formats can be  added without modifying existing code
    
    """
    _checkers: Dict[str, Callable] = {}
    
    def __init__(self, config:Dict):
        super().__init__(config)
        self.name = "StructureCheck"
        
        
    @classmethod
    def register_format(cls, format:str, checker_func: Callable) -> None:
        """Register a format-specific checker."""
        
        cls._checkers[format] = checker_func
    def check_file(self, filepath: Path) -> bool:
        """Does not care about the file """
        return True    
        
    def check_data(self, data :Any, format: str ="json") -> bool:
        """Validate the structure of the data"""
        rules = self.config.get('content_validation', {}).get(format, {})
        if not rules:
            return True
        
        checker = self._checkers.get(format)
        if checker:
            return checker(data, rules)
        return True
    @staticmethod
    def _check_json(data: Any, rules: Dict) -> bool:
        """check json-specific structure limits"""
        
        if StructureCheck.get_depth(data) > rules.get('max_depth', 10):
            return False
        if StructureCheck.get_max_array_size(data) > rules.get('max_array_size', 10000):
            return False
        if StructureCheck.get_max_string_length(data) > rules.get('max_size_string', 10000):
            return False
        if StructureCheck.get_max_object_keys(data) > rules.get('max_object_keys', 1000):
            return False
        return True
    @staticmethod
    def get_depth(obj: Any, depth: int = 0) -> int:
        """ Calculate maximum nesting depth (Duck typing
        """
        if not StructureCheck._is_container(obj):
            return depth 
        if StructureCheck._is_empty(obj):
            return depth
        if hasattr(obj, 'items') and callable(obj.items):
            return max(StructureCheck.get_depth(v, depth + 1) for v in obj.values())
        
        if hasattr(obj, '__iter__'):
            return max(StructureCheck.get_depth(item, depth + 1) for item in obj)
        return depth
    @staticmethod
    def get_max_array_size(obj: Any) -> int:
        """Get maximum array size (duck typing)"""
        if hasattr(obj, '__len__') and hasattr(obj, '__iter__'):
            size = len(obj)
            for item in obj:
                size = max(size, StructureCheck.get_max_array_size(item))
            return size
        if hasattr(obj, 'items') and callable(obj.items):
            size = 0
            for value in obj.values():
                size = max(size, StructureCheck.get_max_array_size(value))
            return size
        return 0
    @staticmethod
    def get_max_string_length(obj: Any) -> int:
        """Get maximum string length (duck typing)"""
        if hasattr(obj, '__str__'):
            return len(str(obj))
        if hasattr(obj, '__iter__') and not hasattr(obj, '__str__'):
            max_len = 0
            for item in obj:
                max_len = max(max_len, StructureCheck.get_max_string_length(item))
            return max_len
        if hasattr(obj, 'items') and callable(obj.items):
            max_len = 0
            for value in obj.values():
                max_len = max(max_len, StructureCheck.get_max_string_length(value))
            return max_len
        return 0
    
    @staticmethod
    def get_max_object_keys(obj: Any) -> int:
        """Get maximum number of object keys (duck typiing)"""
        if hasattr(obj, 'items') and callable(obj.items):
            size = len(obj)
            for value in obj.values():
                size = max(size, StructureCheck.get_max_object_keys(value))
            return size
        if hasattr(obj, '__iter__') and not hasattr(obj, '__str__'):
            size = 0
            for item in obj:
                size = max(size, StructureCheck.get_max_object_keys(item))
            return size
        return 0
    @staticmethod
    def _is_container(obj: Any) -> bool:
        """check if obj behaves like a container"""
        return hasattr (obj, '__len__') and hasattr(obj, '__getitem__')
    @staticmethod
    def _is_empty(obj: Any) -> bool: 
        """check if obj is empty"""
        return hasattr(obj, '__len__') and len(obj) == 0
    @staticmethod
    def _check_csv(data: Any, rules: Dict) -> bool:
        """check csv-specific structure limits"""
        max_columns = rules.get('max_columns', 100)
        max_rows = rules.get('max_rows', 1000000)
        max_field = rules.get('max_fields_size', 10000)
        
        if hasattr (data, '__iter__') and hasattr(data, '__len__'):
            if len(data) == 0:
                return True
            first_row = None
            for row in data:
                first_row = row
                break
            if first_row is None:
                return True
            if hasattr(first_row, '__len__'):
                if len(first_row) > max_columns:
                    return False
            if hasattr(first_row, 'keys') and callable(first_row.keys):
                if len(first_row.keys()) > max_columns:
                    return False
            if len(data) > max_rows:
                return False
            for row in data:
                if hasattr(row, '__iter__') and not isinstance(row, str):
                    for field in row:
                        if hasattr(field, '__str__'):
                            if len(str(field)) > max_field:
                                return False
        return True                        
         
    @staticmethod  
    def _check_xml(data: Any , rules:Dict) -> bool:
        """check xml-specific structure limits"""
        
        max_depth = rules.get('max_depth', 10)
        max_attributes = rules.get('max_attributes', 100)
        max_elements = rules.get('max_elements', 10000)
        
        if StructureCheck._get_xml_depth(data) > max_depth:
            return False
        if StructureCheck._get_xml_max_attributes(data) > max_attributes:
            return False
        if StructureCheck._get_xml_total_elements(data) > max_elements:
            return False
        return True
    @staticmethod
    def _get_xml_depth(element, depth: int =0) -> int:
        """Calculate xml nesting depth"""
        if not list(element):
            return depth
        return max(
            StructureCheck._get_xml_depth(child, depth + 1)
            for child in element
        )
    @staticmethod
    def _get_xml_max_attributes(element) -> int:
        """Get maximum attributes in any xml element"""
        max_attrs = len(element.attrib)  
        for child in element:
            max_attrs =max(
                max_attrs, StructureCheck._get_xml_max_attributes(child)
            )
        return max_attrs
    @staticmethod
    def _get_xml_total_elements(element) -> int:
        """count total number of xml elements """
        count = 1
        for child in element:
            count += StructureCheck._get_xml_total_elements(child)
        return count
    @staticmethod
    def _check_parquet(data : Any, rules: Dict) -> bool:
        """check parquet-specific structure limits"""
        max_row_groups = rules.get('max_row_groups', 100)
        max_columns = rules.get('max_columns', 100)
        max_rows = rules.get('max_rows', 1000000)
        
        
        if hasattr(data, 'num_row_groups'):
            if data.num_row_groups > max_row_groups:
                return False
        if hasattr(data, 'schema') :
            if len(data.schema) > max_columns:
                return False
        if hasattr(data, 'num_rows'):
            if data.num_rows > max_rows:
                return False
        return True
StructureCheck.register_format('json', StructureCheck._check_json)
StructureCheck.register_format('csv', StructureCheck._check_csv)
StructureCheck.register_format('xml', StructureCheck._check_xml)
StructureCheck.register_format('parquet', StructureCheck._check_parquet)                   
           