from Numeric import *
from tables import *

# Open a new empty HDF5 file
fileh = openFile(name = "array3.h5", mode = "w")
# Get the root group
root = fileh.root

# Create a large array
#a = reshape(array(range(2**16), "s"), (2,) * 16)
a = ones((2,) * 8, "c")
print "About to write array a"
print "  with shape: ==>", a.shape
print "  and typecode ==> %c" % a.typecode()

# Save it on the HDF5 file
hdfarray = fileh.createArray(root, 'carray', a, "Large array")

# Get metadata on the previously saved array
print
print "Info on this object (root.carray):"
print "  shape: ==>", root.carray.shape
print "  title: ==>", root.carray.title
print "  typecode ==>", root.carray.typecode

# Close the file
fileh.close()

# Open the previous HDF5 file in read-only mode
fileh = openFile(name = "array3.h5", mode = "r")
# Get the root group
root = fileh.root

# Get metadata on the previously saved array
print
print "Getting info on retrieved /carray object:"
print "  shape: ==>", root.carray.shape
print "  title: ==>", root.carray.title
print "  typecode ==>", root.carray.typecode

# Get the actual array
#b = fileh.readArray("/carray")
# You can obtain the same result with:
b = root.carray.read()
print
print "Array b read from file"
print "  with shape: ==>", b.shape
print "  and typecode ==>", b.typecode()

# Close the file
fileh.close()