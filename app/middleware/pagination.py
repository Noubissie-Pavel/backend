import json

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.utils.utils import PAGE_LIMIT

error_messages = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}


class ResponseFormattingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        page = int(request.query_params.get("page", 1))
        size = int(request.query_params.get("size", PAGE_LIMIT))
        skip = (page - 1) * size
        limit = size

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_body = response_body.decode("utf-8")

        try:
            response_data = json.loads(response_body)
        except json.JSONDecodeError:
            response_data = response_body

        response_message = getattr(request.state, "response_message", "Request was successful")

        if response.status_code >= 400:
            response_message = error_messages.get(response.status_code, "An error occurred")

        if isinstance(response_data, list):
            total_items = len(response_data)
            total_pages = (total_items // size) + (1 if total_items % size != 0 else 0)

            paginated_data = response_data[skip: skip + limit]

            metadata = {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": size
            }

            formatted_response = {
                "metadata": metadata,
                "status": response.status_code,
                "message": response_message,
                "data": paginated_data
            }
        else:
            formatted_response = {
                "metadata": {},
                "status": response.status_code,
                "message": response_message,
                "data": response_data
            }

        return JSONResponse(content=formatted_response, status_code=response.status_code)
