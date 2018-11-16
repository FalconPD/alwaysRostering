import aiohttp
import logging

class HTTPMixin():
    """
    This mixin provides the HTTP routines we use
    """
    async def request(self, method, url, json, params, data, allow_redirects):
        """
        Perform an HTTP request and do some error checking
        """
        await self.token_bucket.get() # throttle requests
        logging.debug(
            "HTTP {} {} json={} params={} data={} allow_redirects={}".format(
            method, url, json, params, data, allow_redirects)
        )
        resp = await self.session.request(method, url, json=json, params=params,
            data=data, allow_redirects=allow_redirects)
#            proxy='http://localhost:8888', verify_ssl=False)
        logging.debug('HTTP RESPONSE {}'.format(resp.status))
        if resp.status >= 400:
            logging.error('HTTP {}'.format(resp.status))
            sys.exit(1)
        return resp

    async def post(self, url, json=None, params=None, data=None,
        allow_redirects=True):
        """
        Shortcut for HTTP POST
        """
        return await self.request('POST', url, json, params, data,
            allow_redirects)

    async def get(self, url, params=None, allow_redirects=True):
        """
        Shortcut for HTTP GET
        """
        return await self.request('GET', url, None, params, None,
            allow_redirects)
