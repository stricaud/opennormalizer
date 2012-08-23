#!/usr/bin/env python3

## This file is part of OpenNormalizer
## Copyright (C) 2012 Sebastien Tricaud <sebastien@honeynet.org>
## License: DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2, December 2004

import os
import importlib

class Output:
    plugins_dir = os.path.dirname(__file__) + os.sep + "plugins" + os.sep + "output" + os.sep

    outputs = {}

    def __init__(self):
        self.outputs_list = self.get_list()
        self.load_outputs()

    def get_list(self):
        return os.listdir(self.plugins_dir)

    def load_outputs(self):
        # print("Loading slicers...")
        for output in self.outputs_list:
            if not output.startswith('_'):
                modulepath = "on.plugins.output." + output
                self.outputs[output] = importlib.__import__(modulepath, fromlist=['output_w'])

    def get_output(self, output_name):
        return self.outputs[output_name]

    def write(self, output_plugin, normalized_data):
        output = self.outputs[output_plugin]
        # True if data were correcly written
        return output.output_w(normalized_data)

