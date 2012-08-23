#
# Maybe the most basic plugin
#

class OutputPlugin:
    def __init__(self):
        pass

    def start_w(self, normalizer_handler):
        pass

    def output_w(self, normalized_data):
        col = 0
        outbuf = ""
        while col < len(normalized_data):
            colbuf = normalized_data[col].replace("\"", "\\\"")
            outbuf += "\"" + colbuf + "\"" + ";"

            col += 1

        print(outbuf[:-1])

        return True

    def end_w(self):
        pass
