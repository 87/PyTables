"""Small but almost complete example showing the PyTables mode of use.

As a result of execution, a 'tutorial1.h5' file is created. You can
look at it with whatever HDF5 generic utility, like h5ls, h5dump or
h5view.

"""


import sys
from Numeric import *
from tables import *


	#'-**-**-**-**-**-**- user record definition  -**-**-**-**-**-**-**-'

# Define a user record to characterize some kind of particles
class Particle(IsRecord):
    name        = '16s'  # 16-character String
    idnumber    = 'Q'    # unsigned long long (i.e. 64-bit integer)
    TDCcount    = 'B'    # unsigned byte
    ADCcount    = 'H'    # unsigned short integer
    grid_i      = 'i'    # integer
    grid_j      = 'i'    # integer
    pressure    = 'f'    # float  (single-precision)
    energy      = 'd'    # double (double-precision)

print
print	'-**-**-**-**-**-**- file creation  -**-**-**-**-**-**-**-'

# The name of our HDF5 filename
filename = "tutorial1.h5"
    
print "Creating file:", filename

# Open a file in "w"rite mode
h5file = openFile(filename, mode = "w", title = "Test file")

print
print	'-**-**-**-**-**-**- group an table creation  -**-**-**-**-**-**-**-'

# Create a new group under "/" (root)
group = h5file.createGroup("/", 'detector', 'Detector information')
print "Group '/detector' created"

# Create one table on it
table = h5file.createTable(group, 'readout', Particle(), "Readout example")
print "Table '/detector/readout' created"

# Get a shortcut to the record object in table
particle = table.record

# Fill the table with 10 particles
for i in xrange(10):
    # First, assign the values to the Particle record
    particle.name  = 'Particle: %6d' % (i)
    particle.TDCcount = i % 256    
    particle.ADCcount = (i * 256) % (1 << 16)
    particle.grid_i = i 
    particle.grid_j = 10 - i
    particle.pressure = float(i*i)
    particle.energy = float(particle.pressure ** 4)
    particle.idnumber = i * (2 ** 34)  # This exceeds long integer range
    # Insert a new particle record
    table.appendAsRecord(particle)      

# Flush the buffers for table
table.flush()

print
print	'-**-**-**-**-**-**- table data reading & selection  -**-**-**-**-**-'

# Read actual data from table. We are interested in collecting pressure values
# on entries where TDCcount field is greater than 3 and pressure less than 50
pressure = [ x.pressure for x in table.readAsRecords()
	         if x.TDCcount > 3 and x.pressure < 50 ]
print "Last record read:"
print x
print "Field pressure elements satisfying the cuts ==>", pressure

# Read also the names with the same cuts
names = [ x.name for x in table.readAsRecords()
	      if x.TDCcount > 3 and x.pressure < 50 ]

print
print	'-**-**-**-**-**-**- array object creation  -**-**-**-**-**-**-**-'

print "Creating a new group called '/columns' to hold new arrays"
gcolumns = h5file.createGroup(h5file.root, "columns", "Pressure and Name")

print "Creating a Numeric array called 'pressure' under '/columns' group"
h5file.createArray(gcolumns, 'pressure', array(pressure), 
                   "Pressure column selection")

print "Creating another Numeric array called 'name' under '/columns' group"
h5file.createArray('/columns', 'name', array(names),
                   "Name column selection")

# Close the file
h5file.close()
print "File '"+filename+"' created"
