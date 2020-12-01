import pexpect

from django.conf import settings

from .exceptions import TelnetUnexpectedResponse, TelnetConnectionTimeout, TelnetLoginFailed


class TelnetConnectionMiddleware(object):
    def process_request(self, request):
        """Add a telnet connection to all request paths that start with /api/
        assuming we only need to connect for these means we avoid unecessary
        overhead on any other functionality we add, and keeps URL path clear
        for it.
        """
        if not request.path.startswith('/api/'):
            return None

        request.telnet_list = []
        for host, port in settings.JASMIN_HOSTS:
            try:
                telnet_item = pexpect.spawn(
                    "telnet %s %s" %
                    (host, port),
                    timeout=settings.TELNET_TIMEOUT,
                )
                telnet_item.expect_exact('Username: ')
                telnet_item.sendline(settings.TELNET_USERNAME)
                telnet_item.expect_exact('Password: ')
                telnet_item.sendline(settings.TELNET_PW)
            except pexpect.EOF:
                raise TelnetUnexpectedResponse
            except pexpect.TIMEOUT:
                raise TelnetConnectionTimeout

            try:
                telnet_item.expect_exact(settings.STANDARD_PROMPT)
            except pexpect.EOF:
                raise TelnetLoginFailed
            else:
                request.telnet_list.append(telnet_item)
        return None

    def process_response(self, request, response):
        "Make sure telnet connection is closed when unleashing response back to client"
        if hasattr(request, 'telnet'):
            try:
                request.telnet.sendline('quit')
            except pexpect.ExceptionPexpect:
                request.telnet.kill(9)
        return response
