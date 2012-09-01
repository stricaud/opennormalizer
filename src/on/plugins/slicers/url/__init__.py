#!/usr/bin/python3

import sys
from pyfurl.furl import Furl

class SlicerPlugin:
    def __init__(self):
        pass

    def _get_url_val(self, url, field):
        if url[field] is not None:
            return url[field].decode("ascii")

        return ""

    def slice_buffer(self, slicer, buffer_chunk, pdata):
        sbuffer = buffer_chunk.decode("utf-8")

        f = Furl()                  # FIXME: This shall not be called everytime!
        f.decode(sbuffer.encode("ascii"))
        url = f.get()

        retval = []
        n_events = 0
        for column in slicer['columns']:
            for tag in column['tags']:
                if tag == "http-credential":
                    retval.append(self._get_url_val(url, 'credential'))
                    n_events += 1
                    continue
                if tag == "http-domain":
                    retval.append(self._get_url_val(url, 'domain'))
                    n_events += 1
                    continue
                if tag == "http-subdomain":
                    retval.append(self._get_url_val(url, 'subdomain'))
                    n_events += 1
                    continue
                if tag == "http-fragment":
                    retval.append(self._get_url_val(url, 'fragment'))
                    n_events += 1
                    continue
                if tag == "http-host":
                    retval.append(self._get_url_val(url, 'host'))
                    n_events += 1
                    continue
                if tag == "http-resource_path":
                    retval.append(self._get_url_val(url, 'resource_path'))
                    n_events += 1
                    continue
                if tag == "http-tld":                
                    retval.append(self._get_url_val(url, 'tld'))
                    n_events += 1
                    continue
                if tag == "http-query_string":
                    retval.append(self._get_url_val(url, 'query_string'))
                    n_events += 1
                    continue
                if tag == "http-scheme":
                    retval.append(self._get_url_val(url, 'scheme'))
                    n_events += 1
                    continue
                if tag == "http-port":
                    retval.append(self._get_url_val(url, 'port'))
                    n_events += 1
                    continue

        return (n_events, retval)

