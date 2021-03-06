#!/usr/bin/env python

import os
import sys
import time
import signal
import argparse

from datetime import datetime
from plugin_loader import PluginLoader
from multiprocessing import Process, active_children

def sigint(signo, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigint)

class PluginProcess(Process):
    def __init__(self, plugin, result_dir='./'):
        self.start_time = None
        self.plugin = plugin
        self.result_dir = result_dir
        super(PluginProcess, self).__init__()

    def __str__(self):
        return self.plugin.__name__

    def run(self):
        res = os.path.join(self.result_dir, '%s.result' % self.plugin.__name__)
        print res
        out = err = open(res, 'w', 0)

        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

        # redirect stdout and stderr to the log file opened above
        os.dup2(out.fileno(), sys.stdout.fileno())
        os.dup2(err.fileno(), sys.stderr.fileno())

        scraper = self.plugin.get_scraper()
        scraper.scrape()

class ScraperEngine(object):
    def __init__(self, plugin_dir, results_dir='./results/', filename_regexp=None, max_active=5, max_run_time=None):
        self.num_active = 0
        self.max_active = max_active
        self.max_run_time = max_run_time

        self.plugin_loader = PluginLoader(filename_regexp)
        self.plugin_loader.load_plugins([plugin_dir])

        self.process_list = [ PluginProcess(plugin=p, result_dir=results_dir) for p in self.plugin_loader.plugins ]    

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
        while len(self.process_list) > 0 or self.num_active > 0:
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
            self.num_active = len(active_children())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--plugin-directory", help="Plugin directory", required=True)
    parser.add_argument("-i", "--plugin-regexp", help="Only Load plugins that match regexp")
    parser.add_argument("-r", "--results-dir", help="Directory used to store results", default="./results/")
    parser.add_argument("-p", "--max-processes", help="Max number of processes to run concurrently", default=5)

    args = parser.parse_args()

    scraper_engine = ScraperEngine(
        plugin_dir=args.plugin_directory, 
        results_dir=args.results_dir,
        filename_regexp=args.plugin_regexp,
        max_active=args.max_processes
    )

    print 'parent process %d' % os.getpid()
    scraper_engine.run()




