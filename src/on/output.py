#!/usr/bin/env python3

## This file is part of OpenNormalizer
## Copyright (C) 2012 Sebastien Tricaud <sebastien@honeynet.org>
## License: DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2, December 2004

import os
import importlib

class Output:
    plugins_dir = os.path.dirname(__file__) + os.sep + "plugins" + os.sep + "output" + os.sep

    outputs = {}

    def __init__(self, normalizer_handler, output_plugin_name):
        self.output_plugin_name = output_plugin_name
        self.normalizer_handler = normalizer_handler
        self.outputs_list = self.get_list()
        self.load_outputs()
        plugin = self.outputs[self.output_plugin_name]
        self.output_plugin = plugin.OutputPlugin()

    def get_list(self):
        return os.listdir(self.plugins_dir)

    def load_outputs(self):
        # print("Loading slicers...")
        for output in self.outputs_list:
            if not output.startswith('_'):
                modulepath = "on.plugins.output." + output
                module = importlib.__import__(modulepath, fromlist=['OutputPlugin'])
                self.outputs[output] = module

    def get_output(self, output_name):
        return self.outputs[output_name]

    def start(self):
        return self.output_plugin.start_w(self.normalizer_handler)

    def write(self, normalized_data):
        # True if data were correcly written
        return self.output_plugin.output_w(normalized_data)

    def end(self):
        return self.output_plugin.end_w()
