def result(data=None, message='OK', code=200, status=True):
    """
    :param data: The data to respond
    :param message: The message to respond
    :param code: The code of HTTP (2xx, 3xx, 4xx, 5xx)
    :param status: Status is true or false.
    :return: The returned response contains data and code.
    `
    res = {
        'jsonrpc': '2.0',
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    `
    """
    res = {
        'jsonrpc': '2.0',
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code


def error(data=None, message='Failed', code=200, status=False):
    """
    :param data: The data to respond
    :param message: The message to respond
    :param code: The code of HTTP (2xx, 3xx, 4xx, 5xx)
    :param status: Status is true or false.
    :return: The returned response contains data and code.
    `
    res = {
        'jsonrpc': '2.0',
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    `
    """
    res = {
        'jsonrpc': '2.0',
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return res, code
