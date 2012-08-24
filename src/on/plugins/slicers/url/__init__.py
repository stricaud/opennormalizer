#!/usr/bin/python3

import sys
from pyfurl.furl import Furl

def slice_buffer(slicer, buffer_chunk, pdata):
    sbuffer = buffer_chunk.decode("utf-8")

    f = Furl()                  # FIXME: This shall not be called everytime!
    f.decode(sbuffer.encode("ascii"))
    url = f.get()

    retval = []
    n_events = 0
    for column in slicer['columns']:
        for tag in column['tags']:
            if tag == "http-credential":
                retval.append(url['credential'])
                n_events += 1
                continue
            if tag == "http-domain":
                retval.append(url['domain'])
                n_events += 1
                continue
            if tag == "http-subdomain":
                retval.append(url['subdomain'])
                n_events += 1
                continue
            if tag == "http-fragment":
                retval.append(url['fragment'])
                n_events += 1
                continue
            if tag == "http-host":
                retval.append(url['host'])
                n_events += 1
                continue
            if tag == "http-resource_path":
                retval.append(url['resource_path'])
                n_events += 1
                continue
            if tag == "http-tld":
                retval.append(url['tld'])
                n_events += 1
                continue
            if tag == "http-query_string":
                retval.append(url['query_string'])
                n_events += 1
                continue
            if tag == "http-scheme":
                retval.append(url['scheme'])
                n_events += 1
                continue
            if tag == "http-port":
                retval.append(url['port'])
                n_events += 1
                continue
    
    return (n_events, retval)

