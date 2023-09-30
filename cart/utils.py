from rest_framework.response import Response
from rest_framework import status


def create_success_response(data, message):
    return Response({
        'success': 'success',
        'message': message,
        'data': data,
    }, status=status.HTTP_200_OK)


def create_error_response(errors, message=None):
    error_message = {'success': 'error', 'errors': errors}
    if message:
        error_message['message'] = message
    return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
