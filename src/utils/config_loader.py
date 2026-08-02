import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

#Business configuration normal ones
config_path=Path('config/config.yaml')
#Business configuration (Countries)
countries_path=Path('config/countries.yaml')
file_config_path=Path('config/file_config.yaml')


def config_loader() -> Dict[str, Any]:
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"{config_path} does not exists please")  
    except Exception as e:
            print(f"Error", e)
            return {}
        
def load_countries()->List[Dict[str, Any]]:
    try:
        if countries_path.exists():
            with open(countries_path, 'r', encoding='utf-8') as f:
                data=yaml.safe_load(f)
                return data.get('countries', [])        
        else:
            raise FileNotFoundError(f"{countries_path} fole does not exist")  
    except Exception as e:
        print(f"ERROR", e)  
        return []
def load_file_config()->Dict[str,Any]:
    try:
        if file_config_path.exists():
            with open(file_config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"{file_config_path} does not exist yet!!")
    except Exception as e:
        print("Error", e)
        return {}       
        
     
if __name__=="__main__" :
    config=config_loader()
    
    print(f"configuration has been done successful {config['pipeline'] ['name']}")   
    countries=load_countries()
    print(f'loaded countries is {len(countries)}')
    filed=load_file_config()
    print(f"{len(filed)}")
    print(f"{filed.get('general', {})}")