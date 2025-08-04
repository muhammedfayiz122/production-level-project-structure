import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from datetime import datetime
from name_of_project.utils.config_loader import load_config
import os

try:
    from colorlog import ColoredFormatter
except ImportError:
    raise ImportError("Install colorlog: pip install colorlog")

class CustomLogger():
    def __init__(self) -> None:
        config = load_config("dev_logger")
        self.log_level = config['log_level'].upper()
        self.log_max_bytes = config['log_max_bytes'] 
        self.log_backup_counts = config['log_backup_counts']
        self.file_format = config['file_format']
        self.date_format = config['date_format']
        self.console_format = config['console_format']
        
        
        self.log_dir = os.path.abspath(config['log_dir'])
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(
            self.log_dir, f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        )

        self.logger = None
        
    def get_logger(self, name=__name__):
        """
        """
        if self.logger:
            return self.logger # Already initialized
        
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        
        if not logger.handlers:
            # <--- File Handler --->
            file_handler = RotatingFileHandler(
                self.log_file, 
                maxBytes=self.log_max_bytes, 
                backupCount=self.log_backup_counts
            )
            file_formatter = logging.Formatter(
                self.file_format, datefmt=self.date_format
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            # <--- Console Handler --->
            console_handler = StreamHandler()
            console_formatter = ColoredFormatter(
                self.console_format,
                datefmt=self.date_format,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red", 
                }
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            logger.propagate = False
            
        self.logger = logger
        return logger
            
if __name__ == "__main__":
    CustomLogger()
        
        
        
        