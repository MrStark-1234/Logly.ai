import os
from datetime import datetime
from typing import Iterator, Dict, Any
from apache_log_parser import make_parser
from ..core.source import LogSource

class ApacheLogSource(LogSource):
    """Apache logs source"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Apache logs source
        
        Args:
            config: Dictionary containing:
                - log_path: Path to Apache log file
                - log_format: Apache log format (default: combined)
        """
        super().__init__(config)
        self.file = None
        self.parser = None
        
    def connect(self) -> bool:
        """Open the Apache log file"""
        try:
            if not os.path.exists(self.config['log_path']):
                print(f"Log file not found: {self.config['log_path']}")
                return False
                
            self.file = open(self.config['log_path'], 'r')
            format_string = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
            if self.config.get('log_format') == 'common':
                format_string = '%h %l %u %t \"%r\" %>s %b'
                
            self.parser = make_parser(format_string)
            return True
        except Exception as e:
            print(f"Failed to open Apache log file: {str(e)}")
            return False
            
    def read_logs(self, start_time: datetime = None, end_time: datetime = None) -> Iterator[Dict[str, Any]]:
        """
        Read logs from Apache log file within the specified time range
        
        Args:
            start_time: Start time for log retrieval
            end_time: End time for log retrieval
            
        Yields:
            Dictionary containing log event data
        """
        if not self.file or not self.parser:
            raise RuntimeError("Not connected to Apache log file")
            
        for line in self.file:
            try:
                parsed = self.parser(line)
                timestamp = datetime.strptime(
                    parsed['time_received_datetimeobj'].strftime('%Y-%m-%d %H:%M:%S'),
                    '%Y-%m-%d %H:%M:%S'
                )
                
                if start_time and timestamp < start_time:
                    continue
                if end_time and timestamp > end_time:
                    break
                    
                yield {
                    'timestamp': timestamp,
                    'remote_host': parsed['remote_host'],
                    'request_method': parsed['request_method'],
                    'request_url': parsed['request_url'],
                    'status': int(parsed['status']),
                    'response_bytes': parsed['response_bytes_clf'],
                    'user_agent': parsed.get('request_header_user_agent', ''),
                    'referer': parsed.get('request_header_referer', '')
                }
            except Exception as e:
                print(f"Error parsing log line: {str(e)}")
                continue
                
    def close(self):
        """Close the Apache log file"""
        if self.file:
            self.file.close()
            self.file = None
        self.parser = None 