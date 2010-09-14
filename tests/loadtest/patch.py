import sys
import time
from socket import error as SocketError

from funkload import FunkLoadTestCase
from webunit import cookie

FunkLoadTestCase._Old = FunkLoadTestCase.FunkLoadTestCase


class _FunkLoadTestCase(FunkLoadTestCase._Old):

    def put(self, url, params=None, description=None, ok_codes=None):
        self.steps += 1
        self.page_responses = 0
        return self._browse(url, params, description, ok_codes, method='PUT')

    def post(self, url, params=None, description=None, ok_codes=None):
        self.steps += 1
        self.page_responses = 0
        return self._browse(url, params, description, ok_codes, method='POST')

    def get(self, url, params=None, description=None, ok_codes=None):
        self.steps += 1
        self.page_responses = 0
        return self._browse(url, params, description, ok_codes, method='GET')

    def delete(self, url, params=None, description=None, ok_codes=None):
        self.steps += 1
        self.page_responses = 0
        return self._browse(url, params, description, ok_codes, method='DELETE')

    def _connect(self, url, params, ok_codes, rtype, description):
        """Handle fetching, logging, errors and history."""
        rtype = rtype.upper()

        if params is None and rtype == 'POST':
            # enable empty post
            params = []
        t_start = time.time()
        try:
            response = self._browser.fetch(url, params, ok_codes=ok_codes,
                                           key_file=self._keyfile_path,
                                           cert_file=self._certfile_path,
                                           method=rtype)
        except:
            etype, value, tback = sys.exc_info()
            t_stop = time.time()
            t_delta = t_stop - t_start
            self.total_time += t_delta
            self.step_success = False
            self.test_status = 'Failure'
            self.logd(' Failed in %.3fs' % t_delta)
            if etype is HTTPError:
                self._log_response(value.response, rtype, description,
                                   t_start, t_stop, log_body=True)
                if self._dumping:
                    self._dump_content(value.response)

                body = value.response.body
                raise self.failureException, str(value.response) + ' ' + str(body)
            else:
                self._log_response_error(url, rtype, description, t_start,
                                         t_stop)
                if etype is SocketError:
                    raise SocketError("Can't load %s." % url)
                raise
        t_stop = time.time()
        # Log response
        t_delta = t_stop - t_start
        self.total_time += t_delta
        if rtype in ('POST', 'PUT', 'GET'):
            self.total_pages += 1
        elif rtype == 'redirect':
            self.total_redirects += 1
        elif rtype == 'link':
            self.total_links += 1
        if rtype in ('POST', 'GET', 'PUT', 'REDIRECT'):
            # this is a valid referer for the next request
            self.setHeader('Referer', url)
        self._browser.history.append((rtype, url))
        self.logd(' Done in %.3fs' % t_delta)
        self._log_response(response, rtype, description, t_start, t_stop)
        if self._dumping:
            self._dump_content(response)
        return response


FunkLoadTestCase.FunkLoadTestCase = _FunkLoadTestCase

import httplib
import urlparse
import os
from funkload.utils import Data
import cStringIO
from webunit.webunittest import HTTPResponse, HTTPError, VERBOSE

def WF_fetch(self, url, postdata=None, server=None, port=None, protocol=None,
             ok_codes=None, key_file=None, cert_file=None, method=None):

    if method is not None:
        method = method.upper()

    # see if the url is fully-qualified (not just a path)
    t_protocol, t_server, t_url, x, t_args, x = urlparse.urlparse(url)
    if t_server:
        protocol = t_protocol
        if ':' in t_server:
            server, port = t_server.split(':')
        else:
            server = t_server
            if protocol == 'http':
                port = '80'
            else:
                port = '443'
        url = t_url
        if t_args:
            url = url + '?' + t_args
        # ignore the machine name if the URL is for localhost
        if t_server == 'localhost':
            server = None
    elif not server:
        # no server was specified with this fetch, or in the URL, so
        # see if there's a base URL to use.
        base = self.get_base_url()
        if base:
            t_protocol, t_server, t_url, x, x, x = urlparse.urlparse(base)
            if t_protocol:
                protocol = t_protocol
            if t_server:
                server = t_server
            if t_url:
                url = urlparse.urljoin(t_url, url)

    # TODO: allow override of the server and port from the URL!
    if server is None:
        server = self.server
    if port is None:
        port = self.port
    if protocol is None:
        protocol = self.protocol
    if ok_codes is None:
        ok_codes = self.expect_codes
    webproxy = {}

    if protocol == 'http':
        try:
            proxystring = os.environ["http_proxy"].replace("http://", "")
            webproxy['host'] = proxystring.split(":")[0]
            webproxy['port'] = int(proxystring.split(":")[1])
        except (KeyError, IndexError, ValueError):
            webproxy = False

        if webproxy:
            h = httplib.HTTPConnection(webproxy['host'], webproxy['port'])
        else:
            h = httplib.HTTP(server, int(port))
        if int(port) == 80:
            host_header = server
        else:
            host_header = '%s:%s' % (server, port)
    elif protocol == 'https':
        #if httpslib is None:
            #raise ValueError, "Can't fetch HTTPS: M2Crypto not installed"

        # FL Patch -------------------------

        # patched to use the given key and cert file
        h = httplib.HTTPS(server, int(port), key_file, cert_file)

        # FL Patch end  -------------------------

        if int(port) == 443:
            host_header = server
        else:
            host_header = '%s:%s' % (server, port)
    else:
        raise ValueError, protocol

    headers = []
    params = None
    if postdata is not None:
        if method is None:
            method = 'POST'
        if webproxy:
            h.putrequest(method, "http://%s%s" % (host_header, url))
        else:
            # Normal post
            h.putrequest(method, url)
        if postdata:
            if isinstance(postdata, Data):
                # User data and content_type
                params = postdata.data
                headers.append(('Content-type', postdata.content_type))
            else:
                # Check for File upload
                is_multipart = False
                for field, value in postdata:
                    if isinstance(value, Upload):
                        # Post with a data file requires multipart mimeencode
                        is_multipart = True
                        break
                if is_multipart:
                    params = mimeEncode(postdata)
                    headers.append(('Content-type', 'multipart/form-data; boundary=%s'%
                                    BOUNDARY))
                else:
                    params = urlencode(postdata)
                    headers.append(('Content-type', 'application/x-www-form-urlencoded'))
            headers.append(('Content-length', str(len(params))))
    else:
        if method is None:
            method = 'GET'
        if webproxy:
            h.putrequest(method, "http://%s%s" % (host_header, url))
        else:
            # Normal GET
            h.putrequest(method, url)

    # Other Full Request headers
    if self.authinfo:
        headers.append(('Authorization', "Basic %s"%self.authinfo))
    if not webproxy:
        # HTTPConnection seems to add a host header itself.
        # So we only need to do this if we are not using a proxy.
        headers.append(('Host', host_header))

    # FL Patch -------------------------
    for key, value in self.extra_headers:
        headers.append((key, value))

    # FL Patch end ---------------------

    # Send cookies
    #  - check the domain, max-age (seconds), path and secure
    #    (http://www.ietf.org/rfc/rfc2109.txt)
    cookies_used = []
    cookie_list = []
    for domain, cookies in self.cookies.items():
        # check cookie domain
        if not server.endswith(domain):
            continue
        for path, cookies in cookies.items():
            # check that the path matches
            urlpath = urlparse.urlparse(url)[2]
            if not urlpath.startswith(path) and not (path == '/' and
                    urlpath == ''):
                continue
            for sendcookie in cookies.values():
                # and that the cookie is or isn't secure
                if sendcookie['secure'] and protocol != 'https':
                    continue
                # TODO: check for expires (max-age is working)
                # hard coded value that application can use to work
                # around expires
                if sendcookie.coded_value in ('"deleted"', "null"):
                    continue
                cookie_list.append("%s=%s;"%(sendcookie.key,
                                            sendcookie.coded_value))
                cookies_used.append(sendcookie.key)

    if cookie_list:
        headers.append(('Cookie', ' '.join(cookie_list)))

    # check that we sent the cookies we expected to
    if self.expect_cookies is not None:
        assert cookies_used == self.expect_cookies, \
            "Didn't use all cookies (%s expected, %s used)"%(
            self.expect_cookies, cookies_used)


    # write and finish the headers
    for header in headers:
        h.putheader(*header)
    h.endheaders()

    if self.debug_headers:
        for header in headers:
            print "Putting header -- %s: %s" % header

    if params is not None:
        h.send(params)

    # handle the reply
    if webproxy:
        r = h.getresponse()
        errcode = r.status
        errmsg = r.reason
        headers = r.msg
        data = r.read()
        response = HTTPResponse(self.cookies, protocol, server, port, url,
                                errcode, errmsg, headers, data,
                                self.error_content)

    else:
        # get the body and save it
        errcode, errmsg, headers = h.getreply()
        f = h.getfile()
        g = cStringIO.StringIO()
        d = f.read()
        while d:
            g.write(d)
            d = f.read()
        response = HTTPResponse(self.cookies, protocol, server, port, url,
                                errcode, errmsg, headers, g.getvalue(),
                                self.error_content)
        f.close()

    if errcode not in ok_codes:
        if VERBOSE:
            sys.stdout.write('e')
            sys.stdout.flush()
        raise HTTPError(response)

    # decode the cookies
    if self.accept_cookies:
        try:
            # decode the cookies and update the cookies store
            cookie.decodeCookies(url, server, headers, self.cookies)
        except:
            if VERBOSE:
                sys.stdout.write('c')
                sys.stdout.flush()
            raise

    # Check errors
    if self.error_content:
        data = response.body
        for content in self.error_content:
            if data.find(content) != -1:
                msg = "Matched error: %s" % content
                if hasattr(self, 'results') and self.results:
                    self.writeError(url, msg)
                self.log('Matched error'+`(url, content)`, data)
                if VERBOSE:
                    sys.stdout.write('c')
                    sys.stdout.flush()
                raise self.failureException, msg

    if VERBOSE:
        sys.stdout.write('_')
        sys.stdout.flush()
    return response

from funkload import PatchWebunit
from webunit.webunittest import WebFetcher

WebFetcher.fetch = PatchWebunit.WF_fetch = WF_fetch


