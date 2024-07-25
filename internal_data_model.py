# internal_data_model.py
# written with the assistance of Generative AI

import os
import hashlib
from datetime import datetime
import random

class InternalRelationship:
    def __init__(self, source_id, target_id, relationship_type, range_offset, range_size):
        self.source_id = source_id
        self.target_id = target_id
        self.relationship_type = relationship_type
        self.range_offset = range_offset
        self.range_size = range_size

class FileSystemEntry:
    def __init__(self, filename, filepath, write_time, sha256_hash, size_in_bytes):
        self.filename = filename
        self.filepath = filepath
        self.write_time = write_time
        self.sha256_hash = sha256_hash
        self.size_in_bytes = size_in_bytes

def calculate_sha256(file_path):
    """Calculate the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_file_write_time(file_path):
    """Get the write time of a file."""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp).isoformat()

def get_file_size(file_path):
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)

def enumerate_files(directory):
    """Enumerate files in a directory and gather information."""
    file_entries = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            filename = os.path.basename(file_path)
            write_time = get_file_write_time(file_path)
            sha256_hash = calculate_sha256(file_path)
            size_in_bytes = get_file_size(file_path)
            file_entry = FileSystemEntry(filename, file_path, write_time, sha256_hash, size_in_bytes)
            file_entries.append(file_entry)
    return file_entries

# Example usage
if __name__ == "__main__":
    directory = "path_to_directory"  # Replace with the path to the directory you want to enumerate
    entries = enumerate_files(directory)
    for entry in entries:
        print(f"Filename: {entry.filename}")
        print(f"Filepath: {entry.filepath}")
        print(f"Write Time: {entry.write_time}")
        print(f"SHA256: {entry.sha256_hash}")
        print(f"Size in Bytes: {entry.size_in_bytes}\n")

