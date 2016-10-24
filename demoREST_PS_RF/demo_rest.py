"""Module help work with REST service"""
import requests
from config import BASE_URL
import RequestsLogger

class DemoREST(object):
    """Contains several methods work with REST service"""

    @staticmethod
    @RequestsLogger.log_decorator
    def call_basic_auth(base_name, base_password, check_name, check_password):
        """Get response after login attempt at url with credentials specified in arguments

        Args:
            base_name: use for init credentials
            base_password: use for init credentials
            check_name: use for login attempt
            check_password: use for login attempt
        """
        url = '{}/basic-auth/{}/{}'.format(BASE_URL, base_name, base_password)
        response = requests.get(url, auth=(check_name, check_password))
        return response

    @staticmethod
    @RequestsLogger.log_decorator
    def call_get():
        """Get response from response"""
        url = '{}/get'.format(BASE_URL)
        response = requests.get(url)
        return response

    @staticmethod
    @RequestsLogger.log_decorator_multi_lines
    def call_steam(lines_number):
        """Get response with specified number of
        lines in arguments.

        Args:
            lines_number: desirable number of lines in response
        """
        url = '{}/stream/{}'.format(BASE_URL, lines_number)
        response = requests.get(url)
        return response
