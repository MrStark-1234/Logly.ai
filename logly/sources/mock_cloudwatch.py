from datetime import datetime, timezone, timedelta
from typing import Iterator, Dict, Any
import random
from ..core.source import LogSource

class MockCloudWatchSource(LogSource):
    """Mock CloudWatch Logs source for testing"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Mock CloudWatch Logs source
        
        Args:
            config: Dictionary containing:
                - num_events: Number of mock events to generate (default: 100)
        """
        super().__init__(config)
        self.connected = False
        
    def connect(self) -> bool:
        """Simulate connection to AWS CloudWatch"""
        self.connected = True
        return True
            
    def read_logs(self, start_time: datetime = None, end_time: datetime = None) -> Iterator[Dict[str, Any]]:
        """
        Generate mock CloudWatch log events
        
        Args:
            start_time: Start time for log retrieval
            end_time: End time for log retrieval
            
        Yields:
            Dictionary containing mock log event data
        """
        if not self.connected:
            raise RuntimeError("Not connected to Mock CloudWatch")
            
        # Set default time range if not provided
        if not start_time:
            start_time = datetime.now(timezone.utc) - timedelta(hours=1)
        if not end_time:
            end_time = datetime.now(timezone.utc)
            
        num_events = self.config.get('num_events', 100)
        time_range = (end_time - start_time).total_seconds()
        
        # Sample log messages
        messages = [
            "API request completed successfully",
            "User authentication successful",
            "Database query executed in 150ms",
            "Cache miss for key: user_preferences",
            "Memory usage at 75%",
            "New user registration: user123",
            "Background job completed",
            "Config update detected",
            "HTTP GET /api/v1/users - 200 OK",
            "Scheduled maintenance started"
        ]
        
        # Generate mock events
        for i in range(num_events):
            # Generate random timestamp within the time range
            event_time = start_time + timedelta(seconds=random.uniform(0, time_range))
            
            yield {
                'timestamp': event_time,
                'message': random.choice(messages),
                'log_stream_name': 'mock-stream-1',
                'event_id': f'mock-event-{i}'
            }
            
    def close(self):
        """Close the mock connection"""
        self.connected = False 