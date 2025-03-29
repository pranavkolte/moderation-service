from rest_framework.response import Response
from rest_framework import status
import datetime
import pytz
from django.conf import settings

class APIResponse:
    
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK, pagination_data=None):
        """ Standard success response format """
        
        metadata = {
            "timestamp": datetime.datetime.now(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "version": settings.API_VERSION
        }

        if pagination_data is not None:
            metadata.update(pagination_data)
        
        response = {
            "message": message,
            "metadata": metadata,
        }
        
        if data is not None:
            response["data"] = data
            
        return Response(response, status=status_code)
    
    @staticmethod
    def error(message="Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code=None, details=None):
        """ Standard error response format """

        if error_code is None:
            error_codes = {
                400: "BAD_REQUEST",
                401: "UNAUTHORIZED",
                403: "FORBIDDEN",
                404: "NOT_FOUND",
                500: "INTERNAL_SERVER_ERROR"
            }
            error_code = error_codes.get(status_code, "UNKNOWN_ERROR")
        
        metadata = {
            "timestamp": datetime.datetime.now(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "version": settings.API_VERSION
        }
        
        response = {
            "metadata": metadata,
            "message": message,
            "error_code": error_code,
        }
        
        if details:
            response["details"] = details
            
        return Response(response, status=status_code)
    
    @staticmethod
    def not_found(message="Resource not found"):
        """ 404 Not Found response """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
        )
    
    @staticmethod
    def server_error(message="An unexpected error occurred"):
        """ 500 Internal Server Error response """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_SERVER_ERROR",
        )
        
    @staticmethod
    def validation_error(message="Validation error", details=None,):
        """ 400 Validation Error response """
        return APIResponse.error(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details,
        )
