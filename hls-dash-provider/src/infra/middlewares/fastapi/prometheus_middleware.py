from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter

REQUEST_COUNT = Counter(
    "order_service_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"]
)

ERROR_COUNT = Counter(
    "order_service_errors_total",
    "Total number of server errors",
    ["endpoint"],
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        try:
            response = await call_next(request)
        except:
            ERROR_COUNT.labels(endpoint=request.url).inc() 
            raise

        method = request.method
        endpoint = request.url.path
        status_code = str(response.status_code)

        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()

        if status_code.startswith("5"):
            ERROR_COUNT.labels(endpoint=endpoint).inc()        

        return response