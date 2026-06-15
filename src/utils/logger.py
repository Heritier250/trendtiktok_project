#Logging is Black box in an airplane keeping everything happens wheather bad or good
from datetime import datetime
from typing import Optional
import logging
#import logger
import os
import logging.handlers
from pathlib import Path

#LOG CONFIGURATION(Nelly Heritier :system admin settings )
LOG_DIRECTORY=Path('logs')

LOG_FILE=LOG_DIRECTORY / "pipeline.log"

ERROR_LOG_FILE=LOG_DIRECTORY / "errors.log"
#How long to keep logs (My decision as an admin)

MAX_LOG_SIZE_MB= 10

BACK_UP_COUNT= 5

LOG_FORMAT="%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-20s | %(message)s"
DATE_FORMAT="%Y-%m-%d %H:%M:%S"

def set_up_logger(
    name :str,
    log_file:Optional[Path]= None,
    level_name:str='INFO',
    
    console_output=True) -> logging.Logger:
    
    #Create directory in it does not exist yet
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True) 
    if log_file is None:
        log_file=LOG_FILE
    #convert string level to logging constant
    level_map={
        "DEBUG":logging.DEBUG,
        "INFO":logging.INFO,
        "WARNING":logging.WARNING,
        "ERROR":logging.ERROR,
        "CRITICAL":logging.CRITICAL
    }
    log_level=level_map.get(level_name.upper(),logging.INFO )
    #Creating logger
    logger=logging.getLogger(name)
    
    logger.setLevel(log_level) 
    
    #remove any existing handlers (avoid duplication logs)
    logger.handlers.clear()
    #create formatter
    
    formatter=logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    #File handler(write to file -PERSISTENT)
    #like writing on black box
    #Info file handler
    file_handler=logging.handlers.RotatingFileHandler(
        
        log_file,
        
        maxBytes=MAX_LOG_SIZE_MB * 1024 * 1024,
        
        backupCount=BACK_UP_COUNT,
        
        encoding='utf-8')
    
    file_handler.setLevel(log_level)
    
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    #ERROR FILE HANDLER (
        # Note that i have separated files for 
        # avoiding wasting time to look through logs
    error_handler=logging.handlers.RotatingFileHandler(
        ERROR_LOG_FILE, 
        maxBytes=MAX_LOG_SIZE_MB * 1024 * 1024,
        backupCount=BACK_UP_COUNT,
        encoding='utf-8'
        
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    #CONSOLE HANDLERS 
    if console_output:
        console_handler=logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

def get_logger(name:str) -> logging.Logger:
    #get existing one instead of creating new one
    return set_up_logger(name)   
def log_pipeline_start(logger:logging.Logger, pipeline_name:str, version:str):
    #logger.info("=============================Pipelines status============================ ")
    logger.info("=" * 70)
    logger.info(f"Pip status Name :{pipeline_name}  pipeline version :{version}" )
    logger.info(f"Pipeline run at :{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
def log_pipeline_end(logger: logging.Logger, status: str, duration_seconds: float):
    """Log the end of a pipeline run"""
    logger.info("=" * 70)
    logger.info(f"PIPELINE END: {status}")
    logger.info(f"Duration: {duration_seconds:.2f} seconds")
    logger.info(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
     
        
def log_extraction_summary(logger:logging.Logger, results:list ):
    success_count=len(results)
    logger.info(f"Extraction complete : {success_count} countries processed")
    for result in results:
        logger.info(f" - {result.get('name', result.get('country'))}:are seccusseful")
    
def get_log_stats()->dict:
    stats={}
    if LOG_FILE.exists():
        stats['pipeline_log_size_mbs']=round(LOG_FILE.stat().st_size/(1024 * 1024), 2)
        age_delta = datetime.now() - datetime.fromtimestamp(LOG_FILE.stat().st_mtime)
        stats['pipeline_log_age'] = round(age_delta.days, 1)
    if ERROR_LOG_FILE.exists():
        stats['error_log_size_mbs']=round(ERROR_LOG_FILE.stat().st_size/ (1024 * 1024), 2)
    if ERROR_LOG_FILE.exists():
        with open (ERROR_LOG_FILE, "r") as f:
            stats['count_error']=sum(1 for line in  f if 'ERROR' in line)
    return stats


def rotate_logs_manually():
    for handler in logging.root.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            handler.doRollover()
    print("Logs has been rotated manually")
        
if __name__ == "__main__":
    """
    This runs when you execute: python -m src.utils.logger
    It demonstrates how the logger works.
    """
    
    print("\n" + "="*60)
    print("TESTING LOGGER MODULE")
    print("="*60)
    
    # Create a test logger
    logger = set_up_logger("test",level_name="DEBUG")      
        # Log messages at different levels
    logger.debug("This is a DEBUG message (detailed, for developers)")
    logger.info("This is an INFO message (normal operation)")
    logger.warning("This is a WARNING message (something unexpected)")
    logger.error("This is an ERROR message (something failed)")
    logger.critical("This is a CRITICAL message (system may crash)")
    
    # Test pipeline logging
    log_pipeline_start(logger, "Test Pipeline", "1.0.0")
    logger.info("Doing some work...")
    log_pipeline_end(logger, "SUCCESS", 12.5)
    stats = get_log_stats()
    print("\n📊 Log Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Logger test complete!")
    print(f"   Logs written to: {LOG_FILE}")
    print(f"   Errors written to: {ERROR_LOG_FILE}")           