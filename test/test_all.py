"""
Run all test cases.
"""

import sys
import os
import unittest

verbose = 0
if 'verbose' in sys.argv:
    verbose = 1
    sys.argv.remove('verbose')

if 'silent' in sys.argv:  # take care of old flag, just in case
    verbose = 0
    sys.argv.remove('silent')


# This little hack is for when this module is run as main and all the
# other modules import it so they will still be able to get the right
# verbose setting.  It's confusing but it works.
import test_all
test_all.verbose = verbose


def suite():
    test_modules = ['test_basics',
                    'test_create',
                    'test_types',
                    'test_numarray',
                    # if test_tables is before test_tree the memory
                    # consumption grows up to 500 MB
                    # If it is placed after, it remains at 15 MB
                    # I don't know what's happening
		    'test_tree',
                    'test_tables',
		    ]

    # Add test_Numeric only if Numeric is installed
    try:
        import Numeric
        print "Numeric is present. Adding the Numeric test suite."
        test_modules.append("test_Numeric")
    except:
        print "Skipping Numeric test suite"
        
    alltests = unittest.TestSuite()
    for name in test_modules:
        module = __import__(name)
        alltests.addTest(module.suite())
    return alltests


if __name__ == '__main__':
    import tables
    import numarray

    print '-=' * 38
    print "PyTables version:  %s" % tables.__version__
    print "Extension version: %s" % tables.ExtVersion
    print "HDF5 version:      %s" % tables.HDF5Version
    print "numarray version:  %s" % numarray.__version__
    print 'Python version:    %s' % sys.version
    if os.name == 'posix':
        (sysname, nodename, release, version, machine) = os.uname()
        print 'Platform:          %s-%s' % (sys.platform, machine)
    print 'Byte-ordering:     %s' % sys.byteorder
    print '-=' * 38

    unittest.main( defaultTest='suite' )

