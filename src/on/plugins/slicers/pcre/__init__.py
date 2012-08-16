import re
import sys

def slice_buffer(slicer, buffer_chunk):
    sbuffer = buffer_chunk.decode("utf-8")
    m = re.match(slicer['data'], sbuffer)
    if m:
        return m.groups()

    return []

