from Numeric import *
from tables import *

# Open a new empty HDF5 file
fileh = openFile(name = "array2.h5", mode = "w")
# Shortcut to the root group
root = fileh.root

# Create an array
a = array([1, 2.7182818284590451, 3.141592], Float)
print "About to write array:", a
print "  with shape: ==>", a.shape
print "  and typecode ==> %c" % a.typecode()

# Save it on the HDF5 file
hdfarray = fileh.createArray(root, 'carray', a, "Float array")

# Get metadata on the previously saved array
print
print "Info on the object:", root.carray
print "  shape: ==>", root.carray.shape
print "  title: ==>", root.carray.title
print "  typecode ==>", root.carray.typecode

# Close the file
fileh.close()

# Open the previous HDF5 file in read-only mode
fileh = openFile(name = "array2.h5", mode = "r")
# Get the root group
root = fileh.root

# Get metadata on the previously saved array
print
print "Info on the object:", root.carray
print "  shape: ==>", root.carray.shape
print "  title: ==>", root.carray.title
print "  typecode ==>", root.carray.typecode

# Get the actual array
b = root.carray.read()
print
print "Array read from file:", b
print "  with shape: ==>", b.shape
print "  and typecode ==>", b.typecode()

# Close the file
fileh.close()