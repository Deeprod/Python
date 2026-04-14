import shutil
import os
from datetime import datetime

import os
os.chdir(r"C:\temp\github\act-python\Jonathan\Movies")

# Define the source and destination paths
source_file = "df.csv"  # Assumes the script runs from the directory where df.csv is located
destination_folder = "_archive"  # Replace with the actual path

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Get the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Construct the new filename with timestamp
destination_file = os.path.join(destination_folder, f"df_{timestamp}.csv")

# Copy the file
shutil.copy(source_file, destination_file)

print(f"File copied to: {destination_file}")