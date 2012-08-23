#
# Maybe the most basic plugin
#

from datetime import datetime

class OutputPlugin:
    def __init__(self):
        self.nh = None
        self.current_id = 0

    def get_id(self):
        self.current_id += 1
        return self.current_id

    def start_w(self, normalizer_handler):
        print("[\n{")
        self.nh = normalizer_handler
        head = self.nh.get_head()
        print("\"id\":\"%d\"," % (self.get_id()))
        print("\"title\":\"%s\"," % (self.nh.filename))
        print("\"description\":\"%s\"," % (head['datatype']))
        print("\"initial_zoom\":\"39\",")
        print("\"events\":[\n")

        return True

    def output_w(self, normalized_data):
        print("{")
        print("\"id\":\"%d\"," % (self.get_id()))
        service = normalized_data[2]
        log = normalized_data[3].replace("\"", "\\\"")
        time_format = self.nh.get_col(0)['option']['time-format']
        time = normalized_data[0]
        formated_time = datetime.strptime(time, time_format).replace(year = 2012)

        print("\"title\":\"%s\"," % (service))
        print("\"description\":\"%s\"," % (log))
        print("\"startdate\":\"%s\"," % (formated_time.strftime("%Y-%m-%d %H:%M:%S")))
        print("\"high_threshold\":\"50\",")
        print("\"importance\":\"40\",")
        print("\"icon\":\"square_black.png\"")
        print("},")
        return True

    def end_w(self):
        print("{")
        print("\"id\":\"_now\",")
        print("\"title\": \"nowEvent\",")
        print("\"date_display\":\"ho\",")
        print("\"description\":\"present moment\",")
        print("\"startdate\":\"today\",")
        print("\"high_threshold\":\"60\",")
        print("\"importance\":\"40\",")
        print("\"icon\":\"triangle_red.png\",")
        print("\"keepCurrent\":\"start\"")
        print("}")

        print("]") # events: [
        print("}\n]")
        return True

