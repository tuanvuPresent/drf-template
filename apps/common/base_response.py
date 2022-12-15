class BaseResponse:

    def __init__(self, status=True, code=0, message=None, data=None):
        self.status = status
        self.code = code
        self.message = message
        self.data = {
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'data': data,
        }
