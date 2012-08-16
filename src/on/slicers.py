#!/usr/bin/env python3

## This file is part of OpenNormalizer
## Copyright (C) 2012 Sebastien Tricaud <sebastien@honeynet.org>
## License: DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2, December 2004

import os
import imp

import importlib

class SlicersHandler:
    plugins_dir = os.path.dirname(__file__) + os.sep + "plugins" + os.sep + "slicers" + os.sep

    slicers = {}

    def __init__(self):
        self.slicers_list = self.get_list()

    def get_list(self):
        return os.listdir(self.plugins_dir)

    def load_slicers(self):
        print("Loading slicers...")
        for slicer in self.slicers_list:
            if not slicer.startswith('_'):
                modulepath = "on.plugins.slicers." + slicer
                print("\t" + modulepath)
                self.slicers[slicer] = importlib.__import__(modulepath, fromlist=['slice_buffer'])

    def get_slicer(self, slicer_name):
        return self.slicers[slicer_name]
