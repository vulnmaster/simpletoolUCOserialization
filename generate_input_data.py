# generate_input_data.py
# this script generates random filetree data that represents a simple filetree enumeration, this is test data to be processed by uco_serialization.py
# written with the assistance of Generative AI

import json
import os
import hashlib
from datetime import datetime, timedelta
import random

# Define the root directory for the simulated file system
root_directory = "C:\\Users\\OperationsManager\\Documents\\GroceryChain"

# Define some example directories and file types
directories = [
    "Reports",
    "Budgets",
    "Schedules",
    "EmployeeRecords",
    "Inventory",
    "VendorContracts"
]

file_extensions = [
    "docx", "xlsx", "pdf", "txt"
]

def generate_filename():
    """Generate a random filename."""
    return f"{random.randint(100000, 999999)}_{random.choice(['Q1', 'Q2', 'Q3', 'Q4'])}.{random.choice(file_extensions)}"

def generate_filepath(filename):
    """Generate a random file path including the filename."""
    return os.path.join(root_directory, random.choice(directories), filename)

def generate_file_write_time():
    """Generate a random file write time."""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    return start_date + (end_date - start_date) * random.random()

def calculate_sha256(data):
    """Calculate the SHA256 hash of the given data."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

def generate_file_entry(index):
    """Generate a single file entry with necessary attributes."""
    filename = generate_filename()
    filepath = generate_filepath(filename)
    write_time = generate_file_write_time()
    sha256_hash = calculate_sha256(filepath + str(write_time))
    size_in_bytes = random.randint(1, 1000)
    return {
        "filename": filename,
        "filepath": filepath,
        "write_time": write_time.isoformat(),
        "sha256_hash": sha256_hash,
        "size_in_bytes": size_in_bytes
    }

# Generate 100000 file entries
data = [generate_file_entry(i) for i in range(100000)]

# Write the data to input_data.json
with open("input_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Generated 100000 file entries in input_data.json")


