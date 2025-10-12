import logging
import time
from datetime import datetime, timezone
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.setup_logging()

    def setup_logging(self):
        """Configure logging to both file and stdout"""
        logger = logging.getLogger("request_logger")
        logger.setLevel(logging.INFO)

        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()

        formatter = logging.Formatter("%(message)s")

        # File handler
        file_handler = logging.FileHandler("requests.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler (stdout)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        logger.propagate = False
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        # Get client IP and port
        client_ip = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"

        # Get the 'team_name' header value directly
        team_name = request.headers.get("team_name", "NO_TEAM_NAME")

        # Get request method
        request_type = request.method

        # Start timer
        start_time = time.time()

        # Process request and get response
        response = await call_next(request)

        # Get timestamp
        timestamp = datetime.now(timezone.utc).isoformat()

        # Get response status code
        status_code = response.status_code

        # Format the log message
        log_message = f"{request_type} : {client_ip}:{client_port} : {team_name} : {timestamp} : {status_code}"

        # Log the message
        self.logger.info(log_message)

        return response
