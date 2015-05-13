import functools
import imp
import importlib
import inspect
import itertools
import logging
import os
import re
import sys
import time
import unittest
import threading
from os.path import join as opj

import unittest2

import openerp
import openerp.tools as tools
import openerp.release as release
from openerp.tools.safe_eval import safe_eval as eval

def load_information_from_description_file(terp_file):
    """
    :param module: The name of the module (sale, purchase, ...)
    :param mod_path: Physical path of module, if not providedThe name of the module (sale, purchase, ...)
    """
    if terp_file:
        info = {}
        if os.path.isfile(terp_file):
            # default values for descriptor
            info = {
                'application': False,
                'author': '',
                'auto_install': False,
                'category': 'Uncategorized',
                'depends': [],
                'description': '',
                'installable': True,
                'license': 'AGPL-3',
                'post_load': None,
                'version': '1.0',
                'web': False,
                'website': '',
                'sequence': 100,
                'summary': '',
            }
            info.update(itertools.izip(
                'depends data demo test init_xml update_xml demo_xml'.split(),
                iter(list, None)))

            with open(terp_file) as f:
				info.update(eval(f.read()))					
				return info

    #TODO: refactor the logger in this file to follow the logging guidelines
    #      for 6.0
    #_logger.debug('module %s: no %s file found.', module, MANIFEST)
    return {}
	
print "Start Odoo Addons Dependency Check"
import os
import ast
basedir = "addons"
openerp = "__openerp__.py"
addons = []
for dir in os.listdir(basedir):
	addons.append(dir)

for dir in os.listdir(basedir):
	#find __openerp__.py
	#print(dir)
	for innerfile in os.listdir(basedir + "/" + dir):
		if innerfile == openerp:
			#print(dir + "/" + innerfile)
			dict = load_information_from_description_file(basedir + "/" + dir + "/" + innerfile)
			l = dict['depends']
			#print(type(dict['auto_install']))
			#list = dict['depends']
			auto = dict['auto_install']
			
			if auto:
				print 'AutoInstall: ', dir
			
			for a in l:
				#print a
				if a not in addons and a != 'base':
					print dir, a
			
						
		
#print(addons)

