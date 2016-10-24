# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn

"""
Library for response check, which based on [ http://docs.python-requests.org/en/latest| requests ]  library.
"""


def check_status_code(code, response):
    """
    Проверка кода http-ответа.\n\n

    *Args:*\n
    _code_ - ожидаемый код ответа. \n
    _response_ - object [ http://docs.python-requests.org/en/latest/api/#requests.Response | "Response" ]\n\n

    *Examples*:\n
    | *Test cases* | *Action*                          | *Argument*            | *Argument*                | *Argument*  |
    | Simple Test  | RequestsLibrary.Create session    | Alias                 | http://www.example.com    |             |
    |              | ${response}=                      | RequestsLibrary.Get request       | Alias         | /           |
    |              | RequestsChecker.Check Status Code | 204                   | ${response}               |             |
    """

    if response.status_code != int(code):
        BuiltIn().fail("URL: {url}\nResponse status code "
                       "is not equal {code}: {code} != {resp_code}({reason})".format(url=response.url,
                                                                                     code=code,
                                                                                     resp_code=response.status_code,
                                                                                     reason=response.reason))


def common_check(response):
    """
    Выполение основных проверок применительно к http-response.\n\n

    *Args:*\n
    _response_ - object [ http://docs.python-requests.org/en/latest/api/#requests.Response | "Response" ]

    *Examples*:\n
    | *Test cases* | *Action*                          | *Argument*            | *Argument*                | *Argument*  |
    | Simple Test  | RequestsLibrary.Create session    | Alias                 | http://www.example.com    |             |
    |              | ${response}=                      | RequestsLibrary.Get request       | Alias         | /           |
    |              | RequestsChecker.Common Check      | ${response}           |                           |             |
    """

    check_status_code(200, response)
