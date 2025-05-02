import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import json

# Configure the logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(name)s] - %(message)s")
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Get request details
        path = request.url.path
        method = request.method
        query_params = dict(request.query_params)
        
        # Log request body for non-GET requests
        if method != "GET":
            try:
                body = await request.body()
                if body:
                    body_str = body.decode()
                    if body_str:
                        try:
                            body_json = json.loads(body_str)
                            logger.info(f"Request: {method} {path} - Query: {query_params} - Body: {json.dumps(body_json, indent=2)}")
                        except json.JSONDecodeError:
                            logger.info(f"Request: {method} {path} - Query: {query_params} - Body: {body_str}")
            except Exception as e:
                logger.info(f"Request: {method} {path} - Query: {query_params}")
        else:
            logger.info(f"Request: {method} {path} - Query: {query_params}")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            logger.info(f"Response: {method} {path} - Status: {response.status_code} - Time: {process_time:.2f}ms")
            return response
        except Exception as exc:
            process_time = (time.time() - start_time) * 1000
            logger.error(f"Error: {exc} - {method} {path} - Time: {process_time:.2f}ms", exc_info=True)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

def add_logger_middleware(app):
    app.add_middleware(LoggerMiddleware) 