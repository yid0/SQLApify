import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from config.logger import AppLogger
import json
class LoggingMiddleware(BaseHTTPMiddleware):
    
    app_logger = AppLogger(__name__)
    logger = app_logger.get_logger()
    
    async def dispatch(self, request: Request, next):      
    
        start_time = time.time()         
        
        self.logger.info({
            "message": "Incoming request",
            "http_method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host,
            "data": await request.body()
            # request.body(),
            # "headers": self.convert_dict(request.headers)
        })

        response : Response = await next(request)

        response_body = b'' if str(await request.body()) else None
        
        async for chunk in response.body_iterator:
            response_body += chunk
       
        process_time = time.time() - start_time
        body = response_body.decode()
        process_time = time.time() - start_time

        self.logger.info({
            "message": "Outgoing response",
            "status_code": response.status_code,
            "process_time": f"{process_time:1f}s",
            "body": str(body) if str(body) else None,
            # "headers" : self.convert_dict(response.headers)
        })
        
        return Response(content=response_body, status_code=response.status_code, 
            headers=dict(response.headers), media_type=response.media_type)
        
    def convert_dict(self, headers: list) -> dict:
        return {
            k.decode('utf-8') if isinstance(k, bytes) else k: 
            v.decode('utf-8') if isinstance(v, bytes) else v 
            for k, v in headers
            if k.decode('utf-8').lower() not in ["server"]
        }
     