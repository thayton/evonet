#!/usr/bin/env python

import os
import sys
import time
import signal
import random

from datetime import datetime
from plugin_loader import PluginLoader
from multiprocessing import Process, active_children

def sigint(signo, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigint)

class PluginProcess(Process):
    def __init__(self, plugin):
        self.start_time = None
        self.plugin = plugin
        super(PluginProcess, self).__init__()
        
    def run(self):
        print '%s ' % self.plugin, self._name + ' (%d)' % os.getpid()

        scraper = self.plugin.get_scraper()
        scraper.scrape()

class ScraperEngine(object):
    def __init__(self, plugin_dir, filename_regexp=None, max_active=5, max_run_time=None):
        self.num_active = 0
        self.max_active = max_active
        self.max_run_time = max_run_time

        self.plugin_loader = PluginLoader(filename_regexp)
        self.plugin_loader.load_plugins([plugin_dir])

        self.process_list = [ PluginProcess(p) for p in self.plugin_loader.plugins ]    

    def launch_max_active(self):
        '''
        Launch up to max_active processes to run plugins
        '''
        self.num_active = len(active_children())

        while len(self.process_list) > 0 and self.num_active < self.max_active:
            process = self.process_list.pop(0)
            process.start_time = datetime.now()
            process.start()

            self.num_active = len(active_children())
        
    def run(self):
        while len(self.process_list) > 0:
            self.launch_max_active()

            #
            # Monitor for hung processes
            #
            if self.max_run_time:
                for p in active_children():
                    run_time = datetime.now() - p.start_time
                    if p.is_alive() and run_time > self.max_run_time:
                        p.terminate()
                
            time.sleep(1)

if __name__ == '__main__':
    print 'parent process %d' % os.getpid()
    scraper_engine = ScraperEngine(plugin_dir='agents/')
    scraper_engine.run()




