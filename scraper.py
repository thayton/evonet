#!/usr/bin/env python

import sys
import signal
import argparse

from plugin_loader import PluginLoader

def sigint(signo, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigint)

class ScraperEngine(object):
    def __init__(self, plugin_dir, filename_regexp=None):
        self.plugin_dir = plugin_dir
        self.plugin_loader = PluginLoader(filename_regexp)

    def load_plugins(self):
        self.plugin_loader.load_plugins([self.plugin_dir])

    def run(self):
        for plug in self.plugin_loader.plugins:
            scraper = plug.get_scraper()
            scraper.scrape()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--plugin-directory", help="Plugin directory", required=True)
    parser.add_argument("-r", "--plugin-regexp", help="Load plugins that match regexp")

    args = parser.parse_args()
    
    scraper_engine = ScraperEngine(
        plugin_dir=args.plugin_directory, 
        filename_regexp=args.plugin_regexp
    )

    scraper_engine.load_plugins()
    scraper_engine.run()
