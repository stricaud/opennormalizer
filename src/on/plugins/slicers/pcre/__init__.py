import re
import sys


# FIXME: at some point, slicer['data'] must be a compiled regex. 
def slice_buffer(slicer, buffer_chunk, pdata):
    sbuffer = buffer_chunk.decode("utf-8")
    rx = re.compile(slicer['data'])

    try:
        pb = pdata["prepend_buf"]
        if pb != "":
            sbuffer = pdata["prepend_buf"] + sbuffer

        pdata["prepend_buf"] = ""
    except KeyError:
        pdata["prepend_buf"] = ""

    lenbuf = len(sbuffer)
    sbuffer_match_last = lenbuf

    retval = []
    n_events = 0

    m_iter = rx.finditer(sbuffer)
    for m in m_iter:
        retval.append(m.groups())
        sbuffer_match_last = m.end(0)

        n_events += 1

    not_matched_buf = lenbuf - sbuffer_match_last
    if not_matched_buf > 0:
        # We are missing stuff
        pdata["prepend_buf"] = sbuffer[:not_matched_buf]

    return (n_events, retval)

