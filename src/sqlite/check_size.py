import os
import shutil
import sqlite3

# Make a copy of the original database file
shutil.copyfile('original.db', 'copy.db')

# Connect to the copied database file
conn = sqlite3.connect('copy.db')

# Create the B-tree index
conn.execute('CREATE INDEX def ON maps(keys)')

# Calculate the size difference
original_size = os.path.getsize('original.db')
copy_size = os.path.getsize('copy.db')
index_size = copy_size - original_size

# Print the estimated index size
print(f"Estimated B-tree index size: {index_size} bytes")

# Close the connection and remove the copied database file
conn.close()
os.remove('copy.db')

