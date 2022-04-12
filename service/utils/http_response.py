from service.utils.http_constances import success_msg,no_data



def success_create_response(message, data=None):
    if data:
        if not isinstance(data, list):
            data = [data]
        return {"code": 201, "message": message, "data": data}
    else:
        return {"code": 201, "message": no_data}

def duplicate_content_response(message):
    return {"code": 409, "message": message}

def service_unavailable(error):
    return {"code": 503, "message": error}

def not_accepted_response(message):
    return {"code": 406, "message": message}