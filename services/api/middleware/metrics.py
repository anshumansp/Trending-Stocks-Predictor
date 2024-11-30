from prometheus_client import Counter, Histogram, Gauge
import time
from fastapi import Request
from typing import Callable
import psutil

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Business metrics
STOCK_ANALYSIS_DURATION = Histogram(
    'stock_analysis_duration_seconds',
    'Time spent analyzing stocks'
)

SENTIMENT_ANALYSIS_DURATION = Histogram(
    'sentiment_analysis_duration_seconds',
    'Time spent on sentiment analysis'
)

# System metrics
MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage'
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active WebSocket connections'
)

class MetricsMiddleware:
    def __init__(self):
        self.start_time = time.time()
        self.update_system_metrics()

    async def metrics_middleware(
        self,
        request: Request,
        call_next: Callable
    ):
        # Record start time
        start_time = time.time()
        
        # Get the route path for the metric labels
        route = request.url.path
        method = request.method

        try:
            # Process the request
            response = await call_next(request)

            # Record metrics
            REQUEST_COUNT.labels(
                method=method,
                endpoint=route,
                status=response.status_code
            ).inc()

            REQUEST_LATENCY.labels(
                method=method,
                endpoint=route
            ).observe(time.time() - start_time)

            return response

        except Exception as exc:
            # Record failed requests
            REQUEST_COUNT.labels(
                method=method,
                endpoint=route,
                status=500
            ).inc()
            raise exc

    def update_system_metrics(self):
        """Update system metrics periodically"""
        try:
            # Memory usage
            memory = psutil.Process().memory_info()
            MEMORY_USAGE.set(memory.rss)

            # CPU usage
            cpu = psutil.Process().cpu_percent()
            CPU_USAGE.set(cpu)

        except Exception as e:
            print(f"Error updating system metrics: {e}")

    def record_analysis_duration(self, analysis_type: str, duration: float):
        """Record the duration of analysis operations"""
        if analysis_type == 'stock':
            STOCK_ANALYSIS_DURATION.observe(duration)
        elif analysis_type == 'sentiment':
            SENTIMENT_ANALYSIS_DURATION.observe(duration)

    def update_active_connections(self, count: int):
        """Update the number of active WebSocket connections"""
        ACTIVE_CONNECTIONS.set(count)

# Metric recording decorators
def record_stock_analysis_time(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        STOCK_ANALYSIS_DURATION.observe(duration)
        return result
    return wrapper

def record_sentiment_analysis_time(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        SENTIMENT_ANALYSIS_DURATION.observe(duration)
        return result
    return wrapper
