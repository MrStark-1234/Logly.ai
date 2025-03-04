from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any
from datetime import datetime

class LogSource(ABC):
    """Abstract base class for all log sources"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the log source"""
        pass
    
    @abstractmethod
    def read_logs(self, start_time: datetime = None, end_time: datetime = None) -> Iterator[Dict[str, Any]]:
        """Read logs from the source within the specified time range"""
        pass
    
    @abstractmethod
    def close(self):
        """Close the connection to the log source"""
        pass
    
    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 