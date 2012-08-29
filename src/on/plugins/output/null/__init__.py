#
# Maybe the most basic plugin
#

class OutputPlugin:
    def __init__(self):
        pass

    def start_w(self, normalizer_handler):
        pass

    def output_w(self, normalized_data):
        return True

    def end_w(self):
        pass
