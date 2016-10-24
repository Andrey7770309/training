# -*- coding: utf-8 -*-
import json
import decorator
import re
from xml.dom import minidom
from robot.api import logger

"""
Library for logging request and response, which based on [ http://docs.python-requests.org/en/latest| requests ]  library.
"""


def write_log(response, multi_lines_response=False):
    """
    Logging of http-request and response

    *Args:*\n
    _response_ - object [ http://docs.python-requests.org/en/latest/api/#requests.Response | "Response" ]

    *Responce:*\n
    Formatted output of request and response in test log

    Example:
    | *Test cases* | *Action*                          | *Argument*            | *Argument*                | *Argument*  |
    | Simple Test  | RequestsLibrary.Create session    | Alias                 | http://www.example.com    |             |
    |              | ${response}=                      | RequestsLibrary.Get request       | Alias         | /           |
    |              | RequestsLogger.Write log          | ${response}           |                           |             |
    """

    msg = []
    # информация о запросе
    msg.append(
        '> {0} {1}'.format(response.request.method, response.request.url))
    for req_key, req_value in response.request.headers.iteritems():
        msg.append('> {header_name}: {header_value}'.format(header_name=req_key,
                                                            header_value=req_value))
    msg.append('>')
    if response.request.body:
        msg.append(response.request.body)
    msg.append('* Elapsed time: {0}'.format(response.elapsed))
    msg.append('>')
    # информация о ответе
    msg.append('< {0} {1}'.format(response.status_code, response.reason))
    for res_key, res_value in response.headers.iteritems():
        msg.append('< {header_name}: {header_value}'.format(header_name=res_key,
                                                            header_value=res_value))
    msg.append('<')
    # тело ответа
    converted_string = ''
    if response.content:
        # получение кодировки входящего сообщения
        responce_content_type = response.headers.get('content-type')
        if 'application/json' in responce_content_type:
            if multi_lines_response:
                content_lines = response.content.splitlines()
                for i in range(len(content_lines)):
                    response_content = get_decoded_response_body(content_lines[i], responce_content_type)
                    converted_string_new = json.loads(response_content)
                    converted_string_new = json.dumps(converted_string_new, sort_keys=True,
                                                      ensure_ascii=False, indent=4,
                                                      separators=(',', ': '))
                    converted_string = converted_string + converted_string_new + '\n'
            else:
                response_content = get_decoded_response_body(response.content, responce_content_type)
                converted_string = json.loads(response_content)
                converted_string = json.dumps(converted_string, sort_keys=True,
                                              ensure_ascii=False, indent=4,
                                              separators=(',', ': '))
        elif 'application/xml' in responce_content_type:
            if multi_lines_response:
                content_lines = response.content.splitlines()
                for i in range(len(content_lines)):
                    response_content = get_decoded_response_body(content_lines[i], responce_content_type)
                    xml = minidom.parseString(response_content)
                    converted_string_new = xml.toprettyxml()
                    converted_string = converted_string + converted_string_new + '\n'
        else:
            if multi_lines_response:
                content_lines = response.content.splitlines()
                for i in range(len(content_lines)):
                    response_content = get_decoded_response_body(content_lines[i], responce_content_type)
                    msg.append(response_content)
    # вывод сообщения в лог
    logger.info('\n'.join(msg))
    if converted_string:
        logger.info(converted_string)


def get_decoded_response_body(response_content, responce_content_type):
    match = re.findall(re.compile('charset=(.*)'),
                       responce_content_type)
    # перекодирование тела ответа в соответствие с кодировкой, если она присутствует в ответе
    if len(match) == 0:
        return response_content
    else:
        responce_charset = match[0]
        return response_content.decode(responce_charset)


def _log_decorator(func, *args, **kwargs):
    response = func(*args, **kwargs)
    write_log(response)
    return response


def _log_decorator_multi_lines(func, *args, **kwargs):
    response = func(*args, **kwargs)
    write_log(response, True)
    return response


def log_decorator(func):
    """
    Decorator for http-requests. Logging request and response.
    Decorated function must return response object [ http://docs.python-requests.org/en/latest/api/#requests | Response ]

    Example:

    | @RequestsLogger.log_decorator
    | def get_data(alias, uri)
    |     response = _request_lib_instance().get_request(alias, uri)
    |     return response

    Output:
    Formatted output of request and response in test log
    """

    func.cache = {}
    return decorator.decorator(_log_decorator, func)


def log_decorator_multi_lines(func):
    """
    Decorator for http-requests. Logging request and multi lines response.
    Decorated function must return response object [ http://docs.python-requests.org/en/latest/api/#requests | Response ]

    Example:

    | @RequestsLogger.log_decorator_multi_lines
    | def get_data(alias, uri)
    |     response = _request_lib_instance().get_request(alias, uri)
    |     return response

    Output:
    Formatted output of request and response in test log
    """

    func.cache = {}
    return decorator.decorator(_log_decorator_multi_lines, func)
