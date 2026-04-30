from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import sys
import time

logger.remove()
logger.add("logs/order_app.log", level="INFO")
logger.add(sys.stdout, level="DEBUG")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"{request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Error while handling request: {e}")
            raise

        duration = (time.time() - start_time) * 1000
        status_code = response.status_code
        log_messsage = f"{request.method} {request.url} - {response.status_code} ({duration:.2f} ms)"
        
        if 200 <= status_code < 300:
            logger.success(log_messsage)
        elif 300 <= status_code < 400:
            logger.warning(log_messsage)
        elif 400 <= status_code < 500:
            logger.error(log_messsage)
        elif 500 <= status_code < 600:
            logger.exception(log_messsage)
        else:
            logger.info(log_messsage)
        

        return response
