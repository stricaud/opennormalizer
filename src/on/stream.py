#!/usr/bin/env python3

## This file is part of OpenNormalizer
## Copyright (C) 2012 Sebastien Tricaud <sebastien@honeynet.org>
## License: DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2, December 2004

class Stream2EventsStream:
    """
    This is a major class, transforming a stream of data (coming from a file, socket etc.) into a normalized array (event)
    """
    max_streambuf = 5        # How far shall we collect data until we give up
    count_streambuf = 0
    collected_buffer = b''

    def __init__(self, normalizedHandler, slicerHandler):
        self.nh = normalizedHandler
        self.sh = slicerHandler

    def _flush_collected_stream(self):
        self.count_streambuf = 0
        self.collected_buffer = b''

    def _normalize(self):
        for slicer_t in self.nh.get_slicers():
            s = self.sh.get_slicer(slicer_t['type'])
            sliced_buf = s.slice_buffer(slicer_t, self.collected_buffer)
        
        return sliced_buf

    def _need_to_collect_more(self, data):
        self.collected_buffer += data
        self.count_streambuf += 1
        return []

    def get(self, data, terminate=False):
        if not terminate:
            if self.count_streambuf == self.max_streambuf:
                # We collected enough, so we normalize
                self.collected_buffer += data
                (n_events, normalized) = self._normalize()
                self._flush_collected_stream()
            else:
                normalized = self._need_to_collect_more(data)
                n_events = 0
        else:                   # if not terminate
            if self.count_streambuf < self.max_streambuf:
                self.collected_buffer += data
                (n_events, normalized) = self._normalize()
                self._flush_collected_stream()
        
        return (n_events, normalized)
