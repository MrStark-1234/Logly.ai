import boto3
from datetime import datetime, timezone
from typing import Iterator, Dict, Any
from ..core.source import LogSource

class CloudWatchLogSource(LogSource):
    """AWS CloudWatch Logs source"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize CloudWatch Logs source
        
        Args:
            config: Dictionary containing:
                - aws_access_key_id: AWS access key ID
                - aws_secret_access_key: AWS secret access key
                - region_name: AWS region name
                - log_group_name: CloudWatch Log Group name
                - log_stream_name: CloudWatch Log Stream name (optional)
        """
        super().__init__(config)
        self.client = None
        
    def connect(self) -> bool:
        """Establish connection to AWS CloudWatch"""
        try:
            self.client = boto3.client(
                'logs',
                aws_access_key_id=self.config.get('aws_access_key_id'),
                aws_secret_access_key=self.config.get('aws_secret_access_key'),
                region_name=self.config.get('region_name')
            )
            return True
        except Exception as e:
            print(f"Failed to connect to AWS CloudWatch: {str(e)}")
            return False
            
    def read_logs(self, start_time: datetime = None, end_time: datetime = None) -> Iterator[Dict[str, Any]]:
        """
        Read logs from CloudWatch within the specified time range
        
        Args:
            start_time: Start time for log retrieval
            end_time: End time for log retrieval
            
        Yields:
            Dictionary containing log event data
        """
        if not self.client:
            raise RuntimeError("Not connected to AWS CloudWatch")
            
        kwargs = {
            'logGroupName': self.config['log_group_name'],
            'startTime': int(start_time.timestamp() * 1000) if start_time else None,
            'endTime': int(end_time.timestamp() * 1000) if end_time else None,
        }
        
        if 'log_stream_name' in self.config:
            kwargs['logStreamNames'] = [self.config['log_stream_name']]
            
        try:
            paginator = self.client.get_paginator('filter_log_events')
            for page in paginator.paginate(**kwargs):
                for event in page.get('events', []):
                    yield {
                        'timestamp': datetime.fromtimestamp(event['timestamp'] / 1000, tz=timezone.utc),
                        'message': event['message'],
                        'log_stream_name': event['logStreamName'],
                        'event_id': event['eventId']
                    }
        except Exception as e:
            print(f"Error reading CloudWatch logs: {str(e)}")
            
    def close(self):
        """Close the CloudWatch connection"""
        self.client = None 