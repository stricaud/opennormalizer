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

    pdata = {}

    def __init__(self, normalizedHandler, slicerHandler):
        self.nh = normalizedHandler
        self.sh = slicerHandler

    def _flush_collected_stream(self):
        self.count_streambuf = 0
        self.collected_buffer = b''

    def get_slicer(self, slicer_id):
        return self.nh.get_slicers()[slicer_id]

    def _get_root_slicer(self):
        return self.get_slicer(0)

    def _normalize_subslice(self, slicer, data):
        s = self.sh.get_slicer(slicer['type'])
        (n_events, sliced_buf) = s.slice_buffer(slicer, data, None)

        return (n_events, sliced_buf)

    def _normalize_line(self, slicer, main_sliced_buf):
        line_n = 0

        for line in main_sliced_buf:
            col_n = 0
            for col in slicer['columns']:
                if col['slicer'] is not None:
                    slicer_id = col['slicer-id']
                    child_slicer = self.get_slicer(slicer_id)
                    (sub_n_events, subsliced_buf) = self._normalize_subslice(child_slicer, line[col_n].encode('utf-8'))
                    line.pop(col_n)
                    for el in subsliced_buf.__reversed__():
                        line.insert(col_n, el)

                col_n += 1

            line_n += 1

        return main_sliced_buf

    def _normalize(self, slicer):
        s = self.sh.get_slicer(slicer['type'])
        (n_events, main_sliced_buf) = s.slice_buffer(slicer, self.collected_buffer, self.pdata)

        main_sliced_buf = self._normalize_line(slicer, main_sliced_buf)

        return (n_events, main_sliced_buf)

    def _need_to_collect_more(self, data):
        self.collected_buffer += data
        self.count_streambuf += 1
        return []

    def get(self, data, terminate=False):
        n_events = 0
        normalized = []

        if not terminate:
            if self.count_streambuf == self.max_streambuf:
                # We collected enough, so we normalize
                self.collected_buffer += data
                (n_events, normalized) = self._normalize(self._get_root_slicer())
                self._flush_collected_stream()
            else:
                normalized = self._need_to_collect_more(data)
                n_events = 0
        else: # if not terminate
            # if self.count_streambuf < self.max_streambuf:
            self.collected_buffer += data
            try:
                (n_events, normalized) = self._normalize(self._get_root_slicer())
            except ValueError:
                print("Nothing was normalized")
            self._flush_collected_stream()
        
        return (n_events, normalized)
