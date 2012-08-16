import re
import sys

# FIXME: at some point, slicer['data'] must be a compiled regex. 
def slice_buffer(slicer, buffer_chunk):
    sbuffer = buffer_chunk.decode("utf-8")
    rx = re.compile(slicer['data'])

    retval = []
    n_events = 0

    m_iter = rx.finditer(sbuffer)
    for m in m_iter:
        retval.append(m.groups())
        n_events += 1

    return (n_events, retval)

