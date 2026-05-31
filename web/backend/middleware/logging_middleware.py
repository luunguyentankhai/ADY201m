import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from web.backend.config.logs_config import logger

class AutoLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "Unknown"
        method = request.method
        url = request.url.path

        logger.info(f"[REQUEST] {method} {url} | IP: {client_ip}")

        try:
            response = await call_next(request)
            
            process_time = time.time() - start_time

            logger.info(
                    f"[RESPONSE] {method} {url} | Status: {response.status_code}"
                    f"Time: {process_time:.4f}s"
            )

            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            process_time = time.time() - start_time

            logger.exception(
                f"[CRASH] {method} {url} | Time: {process_time:.4f}s"
                f"Error: {str(e)}"
            )

            raise e

