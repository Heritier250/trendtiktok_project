import json
import os
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Any
from datetime  import datetime, timedelta
import logging
logger=logging.getLogger(__name__)

class PathBuilder:
    def __init__(self, base_directory:str="data/cache"):
        
        self.base_path=Path(base_directory)
        self.rawpath=self.base_path/"raw"
        self.processedpath=self.base_path/"processed"
        
    def ensure_directory(self) -> None:
        self.rawpath.mkdir(parents=True, exist_ok=True)
        self.processedpath.mkdir(parents=True, exist_ok=True)
       
    def rawpath_for_country(self, country_code:str)-> Path:
        return self.rawpath/country_code
    
    def generate_filename(self, suffix:str="")->str:
        
        current_time=datetime.now()
        
        timestamp=current_time.strftime("%Y%m%d-%H%M%S")
        if suffix:
            return f"{suffix}-{timestamp}.json"
        else:
            return f"{timestamp}.json"
    def get_raw_path(self, country_code:str="", suffix:str="")-> Path:
        
        if not country_code:
               raise ValueError("country_code is required")
                
                # Get the country directory
        country_dir = self.rawpath_for_country(country_code)
                
                # If no suffix, just return the directory
        if not suffix:
                    return country_dir
                
                # If suffix provided, build full file path
        filename = self.generate_filename(suffix)
        return country_dir / filename   
        
        
    # First, ensure we have a country_code
                
class Serializer:
    @staticmethod
    def save(data, filepath):
        if not data:
            return
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump( data, f, indent=4, ensure_ascii=False)
# Create instances
    @staticmethod
    def load(filepath:Path):
        if not filepath.exists():
            logger.warning(f"{filepath} file not found  ")
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                loaded_data=json.load(file)
                return loaded_data
        except json.JSONDecodeError:
            logger.error(f"{filepath} has been corrupted at {datetime.now().strftime("%Y%m%d-%H%M%S")}")
            return {}
        except PermissionError:
            logger.error(f"{filepath} can be accessed {datetime.now().strftime("%Y%m%d-%H%M%S")}")
            return {}
        except Exception as e:
            logger.error(f"{e} :occered at {datetime.now().strftime("%Y%m%d-%H:%M%S")}")
            return {}
        
    @staticmethod      
    def exists(filepath):
        return filepath.exists()
    
    @staticmethod
    def get_size_in_kb(filepath):
        
        if not filepath.exists():
            return 0.0
        
        get_byte=filepath.stat().st_size
        return get_byte/1024
            
class Agechecker:
    def __init__(self, path_builder:PathBuilder):
        
        self.path_builder=path_builder
        
    def get_age_fle_hours(self, filepath:Path):
        
        if not filepath.exists():
            return float('inf')
        #getting the last modifacation time of file 
        mtime=filepath.stat().st_mtime
        #getting the age in form datedelta 
        #fromtimestamp : trying to convert unixtimestamp into datetime objects
        age=datetime.now() - datetime.fromtimestamp(mtime)
        #total_second() :convert datedelta into normal seconds
        return age.total_seconds()/ 3600
    
    def is_flesh(self, filepath:Path, max_hours:int=6):
        return self.get_age_fle_hours(filepath) < max_hours
    
    def latest_raw(self, country_code:str)-> Optional[Path]:
        
        country_di= self.path_builder.rawpath_for_country(country_code)
        
        if not country_di.exists():
            return None
        
        files=list(country_di.glob("*.json"))
        
        if not files:
            return None
        
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        return files[0]
    
    def get_latest_raw_age_hour(self, country_code):
        latest=self.latest_raw(country_code)
        
        if not latest:
            return None
        return self.get_age_fle_hours(latest)

