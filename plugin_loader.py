#!/usr/bin/env python

import os
import re
import sys
import imp
import logging

from urlparse import urlparse

class FileFilter:
    """
    Class for recursively loading a list of files, filtered by their extension, from a given a directory
    """
    def __init__(self, filename_regexp=None):
        if filename_regexp:
            r = re.compile(filename_regexp)
            self.filename_filter = r.search
        else:
            self.filename_filter=None

    def get_files(self, directory, ext):
        """ 
        Recursively descend into a directory and
        return all plugin files found 
        """
        def is_notdir(f):
            return os.path.isdir(f) is False

        def is_plugin(f):
            return os.path.splitext(f)[1] == ext

        dirents = [ os.path.join(directory, f) for f in os.listdir(directory) if not f.startswith('.')]

        ret = filter(is_notdir, dirents)
        ret = filter(is_plugin, ret)

        if self.filename_filter:
            ret = [f for f in ret if self.filename_filter(os.path.basename(f))]
            
        for d in filter(os.path.isdir, dirents):
            ret.extend(self.get_files(d, '.py'))

        return ret

class PluginLoader:
    """
    Class for loading agent plugins. 
    """
    def __init__(self, filename_regexp=None):
        self.plugins = []
        self.file_filter = FileFilter(filename_regexp=filename_regexp)
        self.logger = logging.getLogger('evonet.PluginLoader')
        self.logger.setLevel(logging.DEBUG)

    def load_plugins(self, dirlist, exclude=[]):
        """
        Load plugins from files unless they are in the exclude list
        """
        for directory in dirlist:
            files = self.file_filter.get_files(directory, '.py')
            for f in files:
                plug = self.load_plugin(f)
                if self.plug_name(plug) not in exclude:
                    #
                    # Plugin can mark itself to be skipped by setting
                    # the 'skip' attribute. 
                    #
                    if getattr(plug, 'skip', None) != None:
                        print 'Skipping plugin %s' % plug
                        continue

                    self.plugins.append(plug)

    def load_plugin(self, path):
        modname = os.path.splitext(os.path.basename(path))[0]
        try:
            mod = imp.load_source(modname, path)
            return mod
        except ImportError, e:
            self.logger.error("load_plugin failed - error:", e)
    
    def get_plugin(self, site):
        """ Return the plugin used for scraping people from the given site """
        for plugin in self.plugins:
            if site == plugin.__name__:
                return plugin
            
        return None

    def plug_name(self, plug_module):
        netloc = urlparse(plug_module.PLUGINFO['url']).netloc
        tld = netloc.rsplit('.', 1)[1]

        name = plug_module.__name__
        return name
        
if __name__ == '__main__':
    pldr = PluginLoader(filename_regexp=r'.*')
    pldr.load_plugins(['agents/'])

    plug = pldr.get_plugin('weightmans')

    scraper = plug.get_scraper()
    scraper.scrape()

