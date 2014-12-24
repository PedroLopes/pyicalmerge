#!/bin/env/python
# -*- coding: utf8 -*-
# Combine iCalendar files
# $Id$
# uses http://vobject.skyhouseconsulting.com/

import os
import sys
import traceback
import datetime
import glob
import codecs

from ConfigParser import ConfigParser
#import configparser
from optparse import OptionParser, Option, OptionGroup

# 3rd party libs
import vobject

__AUTHOR__ = u"Pekka Järvinen // Modded by Pedro Lopes"
__YEAR__ = "2010 (original) // 2014 (Mod)"
__VERSION__ = "0.0.2 (advanced one version from original)"


DEBUG = False
counterCALSCALE = 0

if __name__ == "__main__":
    banner  = u" %s" % (__VERSION__)
    banner += u" (c) %s %s" % (__AUTHOR__, __YEAR__)

    examples = []
    examples.append("")

    usage = "\n".join(examples)

    parser = OptionParser(version="%prog " + __VERSION__, usage=usage, description=banner)

    parser.add_option("--files", "-f", action="store", type="string", dest="files", help="Files match (Default: *.ics)", default="*.ics")
    parser.add_option("--ical", "-i", action="store", type="string", dest="icalfile", help="iCalendar file output")

    (options, args) = parser.parse_args()

    if options.icalfile == "":
        options.icalfile = None


    if options.icalfile != None:
        options.icalfile = os.path.realpath(options.icalfile)

        files = glob.glob(options.files)

        combinedCalendar = vobject.iCalendar()

        for i in files:
            if ( DEBUG):
	       print ("Opening '%s'.." % i)
            f = open(i, 'rb')
            if ( DEBUG):
              print ("Reading '%s'.." % i)
            contents = f.read()
            out = open('%s_modded.ics' % i,'w')
            s = []
            for sentence in contents:
                s.append(sentence)
		if (sentence == "\n"):
		  check_property = (''.join([str(x) for x in s]))
                  check_property = check_property.replace("X-RICAL-TZSOURCE=", "");
		  if (check_property.find('CALSCALE') != -1): #CALSCALE
                    counterCALSCALE+=1 #increment that we have seen a CALSCALE
		    if (counterCALSCALE <= 1):
	              out.write(check_property) #first one we encounter, safe to print
                    elif (DEBUG): 
                      print("Avoiding further CALSCALE")
	          else: #another property, totally safe to write
		    if (DEBUG):
		      print("WRITE:"+check_property)
                    out.write(check_property)
                  s = []
            out.close()
            out = open('%s_modded.ics' % i,'r')
            contents = out.read()
	    contents = contents.decode('utf-8')
            f.close()

            components = vobject.readComponents(contents, validate=True)

            for component in components:
                for child in component.getChildren():

                    add_entry = True

                    if child.name == 'VERSION':
                        add_entry = False

                    if child.name == 'PRODID':
                        add_entry = False

                    if add_entry:
                        combinedCalendar.add(child)
            
                

        # Write iCal file
        if (DEBUG): 
	  print ("Writing iCalendar file '%s'.." % options.icalfile)
        f = open(options.icalfile, 'wb')
        print(combinedCalendar)
        f.write(combinedCalendar.serialize())
        f.close()
        sys.exit(0)
    sys.exit(1)
