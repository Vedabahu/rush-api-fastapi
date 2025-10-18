import logging
import time
from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import JSONResponse
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
        client_path = request.url.path if request.url else "unknown"

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
        log_message = f"{request_type} {client_path} : {client_ip}:{client_port} : {team_name} : {timestamp} : {status_code}"

        # Log the message
        self.logger.info(log_message)

        return response


# Store IP → block_until timestamp
blocked_ips = {}
DELAY_SECONDS = 10  # Example delay


class BlockOn404Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        # Check if IP is currently blocked
        blocked_until = blocked_ips.get(client_ip)
        if blocked_until:
            if time.time() < blocked_until:
                remaining = int(blocked_until - time.time())
                return JSONResponse(
                    {
                        "error": f"You have visited a wrong node. Wait for {remaining} seconds before proceeding."
                    },
                    status_code=403,
                )
            else:
                # Block expired, remove entry
                blocked_ips.pop(client_ip, None)

        response = await call_next(request)
        # If response is 404, add IP to blocked list
        if response.status_code == 404:
            blocked_ips[client_ip] = time.time() + DELAY_SECONDS

        return response


class RequireTeamNameMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Skip validation for /rules endpoint
        if request.url.path == "/rules":
            return await call_next(request)

        # Check for 'team_name' header
        team_name = request.headers.get("team_name")
        if not team_name:
            return JSONResponse(
                {"error": "Missing required header: 'team_name'"},
                status_code=403,
            )

        # Continue processing
        return await call_next(request)
