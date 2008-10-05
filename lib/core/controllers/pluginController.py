#!/usr/bin/env python
#
#   hostmap
#   http://hostmap.sourceforge.net/
#
#   Author:
#    Alessandro `jekil` Tanasi <alessandro@tanasi.it>
#
#   License:
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA



import os
import lib.core.outputDeflector as log



class plugin:
    """ 
    Plugins engine that handle an event based host discovery

    @author: Alessandro Tanasi
    """



    def __init__(self,  debug = False):
        """
        """
        
        # Tag used in all output messages
        self.tag = "PLUGIN"
        
        # Host discovery debug mode
        self.debug = debug
        
        # Directory of plugins
        # TODO: import from settings
        self.pluginDir = "discovery"
        
        # Preventive check
        self.precheck()
        
        # Plugin dependencies array
        self.pluginsByIp = []
        self.pluginsByDomain = []
        self.pluginsByNameserver = []
        self.pluginsByHostname = []
        
        # Populate dependencies
        self.buildDeps()



    def precheck(self):
        """
        Preventive check for plugin directory
        """
        
        if os.path.exists(self.pluginDir):
            if self.debug: log.out.debug("Plugin directory exist",  time=True,  tag=self.tag)
        else:
            if self.debug: log.out.debug("Plugin directory not exist",  time=True,  tag=self.tag)
            # TODO: raise exception
        
        
    def getPlugins(self):
        """
        Scan plugins directory and make a list of available plugins
        
        @returns: array with list of plugins
        """
        
        # List of plugins in category.plugin syntax, useful for importing
        plugins = []
        
        # Get categorie's names
        dirList = [ f for f in os.listdir(self.pluginDir) ] 
        
        # Remove some stuff
        try:
            dirList.remove ("__init__.py")
            dirList.remove ("__init__.pyc")
            dirList.remove (".svn")
        except ValueError:
            pass
        
        # Get file's names
        for dir in dirList:
            for file in os.listdir(self.pluginDir + os.path.sep + dir):
                # Skip some stuff
                if file == ".svn" or file == "__init__.py":
                    continue
                
                # Get plugins name
                if os.path.splitext(file)[1] == ".py":
                    plugin = self.pluginDir + "." + dir + "." + os.path.splitext(file)[0]
                    plugins.append(plugin)
                    if self.debug: log.out.debug("Found plugin: %s" % plugin,  time=True,  tag=self.tag)
        
        return plugins



    def factory(self, ModuleName, *args):
        import sys
        __import__(ModuleName)
        aModule = sys.modules[ModuleName]
        className = ModuleName.split('.')[len(ModuleName.split('.'))-1]
        aClass = getattr( aModule , className )
        return apply(aClass, args)



    def buildDeps(self):
        """
        Build plugin's dependencies
        """
        
        for plugin in self.getPlugins():
            try:
                # Istantiate a the plugin
                pl = self.factory(plugin)
                
                # Build dependencies array
                deps = pl.require()
            except:
                # TODO: remove plugin from list and log the error
                continue
            
            # Trivial case..
            if deps == "ip":  
                self.pluginsByIp.append(plugin)
                if self.debug: log.out.debug("Plugin %s added to ip queue" % plugin,  time=True,  tag=self.tag)
                
            if deps == "domain":  
                self.pluginsByDomain.append(plugin)
                if self.debug: log.out.debug("Plugin %s added to domain queue" % plugin,  time=True,  tag=self.tag)
                
            if deps == "nameserver":  
                self.pluginsByNameserver.append(plugin)
                if self.debug: log.out.debug("Plugin %s added to nameserver queue" % plugin,  time=True,  tag=self.tag)
                
            if deps == "hostname":  
                self.pluginsByHostname.append(plugin)
                if self.debug: log.out.debug("Plugin %s added to hostname queue" % plugin,  time=True,  tag=self.tag)



    def runByIp(self, hd, ip):
        """
        Run all plugins that depends from ip addresses
        """
        
        for plugin in self.pluginsByIp:
            try:
                # Istantiate a the plugin
                pl = self.factory(plugin)
                    
                # Run
                pl.run(hd,  ip)
            except Exception, e:
                log.out.fatal("Plugin %s get an error. Unhandled exception: %s" % (plugin,  e),  time=True,  tag=self.tag)



    def runByDomain(self, hd, domain):
        """
        Run all plugins that depends from domain
        """
        
        for plugin in self.pluginsByDomain:
            try:
                # Istantiate a the plugin
                pl = self.factory(plugin)
                    
                # Run
                pl.run(hd,  domain)
            except Exception,  e:
                log.out.fatal("Plugin %s get an error. Unhandled exception: %s" % (plugin,  e),  time=True,  tag=self.tag)



    def runByNamserver(self, hd, nameserver):
        """
        Run all plugins that depends from ip nameserver
        """
        
        for plugin in self.pluginsByNameserver:
            try:
                # Istantiate a the plugin
                pl = self.factory(plugin)
                    
                # Run
                pl.run(hd,  ip)
            except Exception,  e:
                log.out.fatal("Plugin %s get an error. Unhandled exception: %s" % (plugin,  e),  time=True,  tag=self.tag)



    def runByHostname(self, hd, hostname):
        """
        Run all plugins that depends from ip hostname
        """
        
        for plugin in self.pluginsByHostname:
            try:
                # Istantiate a the plugin
                pl = self.factory(plugin)
                    
                # Run
                pl.run(hd,  ip)
            except Exception,  e:
                log.out.error("Plugin %s get an error. Unhandled exception: %s" % (plugin,  e),  time=True,  tag=self.tag)
