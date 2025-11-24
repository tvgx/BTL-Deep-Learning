"""
Logger configuration and setup utilities
Provides centralized logging functionality for the entire project
"""
import logging
import logging.config
import os
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class ProjectLogger:
    """Centralized logger for the AI Face Detection project"""
    
    _loggers: Dict[str, logging.Logger] = {}
    _config_loaded = False
    
    @classmethod
    def setup_logging(
        cls, 
        config_path: Optional[str] = None,
        log_level: str = "INFO",
        log_dir: Optional[str] = None
    ) -> None:
        """
        Setup logging configuration
        
        Args:
            config_path: Path to logging configuration file
            log_level: Default log level if no config file
            log_dir: Directory to store log files
        """
        if cls._config_loaded:
            return
            
        # Set default log directory
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
        
        # Create logs directory if it doesn't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Try to load config file
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "logger.yml")
        
        if os.path.exists(config_path):
            cls._load_config_from_file(config_path, log_dir)
        else:
            cls._setup_default_logging(log_level, log_dir)
        
        cls._config_loaded = True
    
    @classmethod
    def _load_config_from_file(cls, config_path: str, log_dir: str) -> None:
        """Load logging configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Update file paths in config to use log_dir
            if 'handlers' in config:
                for handler_name, handler_config in config['handlers'].items():
                    if 'filename' in handler_config:
                        filename = handler_config['filename']
                        # Replace placeholder with actual log directory
                        if filename.startswith('./logs/'):
                            filename = filename.replace('./logs/', f'{log_dir}/')
                        handler_config['filename'] = filename
            
            logging.config.dictConfig(config)
            
        except Exception as e:
            print(f"Failed to load logging config from {config_path}: {e}")
            cls._setup_default_logging("INFO", log_dir)
    
    @classmethod
    def _setup_default_logging(cls, log_level: str, log_dir: str) -> None:
        """Setup default logging configuration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    os.path.join(log_dir, f'app_{timestamp}.log'),
                    encoding='utf-8'
                )
            ]
        )
    
    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        """
        Get logger instance
        
        Args:
            name: Logger name (defaults to caller module name)
            
        Returns:
            Logger instance
        """
        if not cls._config_loaded:
            cls.setup_logging()
        
        if name is None:
            import inspect
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'unknown')
        
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        
        return cls._loggers[name]
    
    @classmethod
    def log_model_info(cls, model_name: str, params: Dict[str, Any]) -> None:
        """Log model information"""
        logger = cls.get_logger('model_info')
        logger.info(f"Model: {model_name}")
        for key, value in params.items():
            logger.info(f"  {key}: {value}")
    
    @classmethod
    def log_training_metrics(
        cls, 
        epoch: int, 
        train_loss: float, 
        val_loss: float, 
        train_acc: float, 
        val_acc: float
    ) -> None:
        """Log training metrics"""
        logger = cls.get_logger('training')
        logger.info(
            f"Epoch {epoch}: "
            f"Train Loss: {train_loss:.4f}, "
            f"Val Loss: {val_loss:.4f}, "
            f"Train Acc: {train_acc:.4f}, "
            f"Val Acc: {val_acc:.4f}"
        )
    
    @classmethod
    def log_data_info(cls, dataset_name: str, num_samples: int, num_classes: int) -> None:
        """Log dataset information"""
        logger = cls.get_logger('data_info')
        logger.info(f"Dataset: {dataset_name}")
        logger.info(f"  Number of samples: {num_samples}")
        logger.info(f"  Number of classes: {num_classes}")
    
    @classmethod
    def log_error(cls, error: Exception, context: str = "") -> None:
        """Log error with context"""
        logger = cls.get_logger('error')
        if context:
            logger.error(f"{context}: {str(error)}", exc_info=True)
        else:
            logger.error(str(error), exc_info=True)


# Convenience functions for easy import
def get_logger(name: str = None) -> logging.Logger:
    """Get logger instance - convenience function"""
    return ProjectLogger.get_logger(name)


def setup_logging(config_path: Optional[str] = None, log_level: str = "INFO") -> None:
    """Setup logging - convenience function"""
    ProjectLogger.setup_logging(config_path, log_level)


def log_info(message: str, logger_name: str = None) -> None:
    """Log info message - convenience function"""
    logger = ProjectLogger.get_logger(logger_name)
    logger.info(message)


def log_warning(message: str, logger_name: str = None) -> None:
    """Log warning message - convenience function"""
    logger = ProjectLogger.get_logger(logger_name)
    logger.warning(message)


def log_error(message: str, logger_name: str = None, exc_info: bool = False) -> None:
    """Log error message - convenience function"""
    logger = ProjectLogger.get_logger(logger_name)
    logger.error(message, exc_info=exc_info)


def log_debug(message: str, logger_name: str = None) -> None:
    """Log debug message - convenience function"""
    logger = ProjectLogger.get_logger(logger_name)
    logger.debug(message)


# Performance logging decorator
def log_execution_time(logger_name: str = None):
    """Decorator to log function execution time"""
    import time
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = ProjectLogger.get_logger(logger_name)
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
                raise
        return wrapper
    return decorator


if __name__ == "__main__":
    # Example usage
    setup_logging()
    
    logger = get_logger(__name__)
    logger.info("Logger setup complete!")
    
    # Test different log levels
    log_info("This is an info message")
    log_warning("This is a warning message")
    log_error("This is an error message")
    log_debug("This is a debug message")
    
    # Test model logging
    ProjectLogger.log_model_info("ResNet50", {
        "layers": 50,
        "parameters": "25.6M",
        "input_size": "224x224"
    })
    
    # Test training logging
    ProjectLogger.log_training_metrics(
        epoch=1,
        train_loss=0.5234,
        val_loss=0.4123,
        train_acc=0.8567,
        val_acc=0.8901
    )