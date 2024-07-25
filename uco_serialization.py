# written with the assistance of Generative AI

import uuid
import json
import argparse
import os
import ijson  # Importing ijson for efficient JSON reading

from internal_data_model import FileSystemEntry, InternalRelationship

# Define namespaces
UCO_CORE = "https://ontology.unifiedcyberontology.org/uco/core/"
UCO_OBSERVABLE = "https://ontology.unifiedcyberontology.org/uco/observable/"
UCO_TYPES = "https://ontology.unifiedcyberontology.org/uco/types/"
UCO_VOCABULARY = "https://ontology.unifiedcyberontology.org/uco/vocabulary/"
EX = "http://example.org/kb/"

class CASEUCO:
    def __init__(self, output_file):
        self.context = {
            "@vocab": "http://example.org/local#",
            "kb": "http://example.org/kb/",
            "uco-core": UCO_CORE,
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-observable": UCO_OBSERVABLE,
            "uco-types": UCO_TYPES,
            "uco-vocabulary": UCO_VOCABULARY,
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        }
        self.output_file = output_file
        self.graph = []

    def generate_uuid(self):
        return str(uuid.uuid4())

    def add_file_system_entry(self, filename, filepath, write_time, sha256_hash, size_in_bytes):
        file_entry_id = f"kb:file_entry-{self.generate_uuid()}"
        content_data_facet_id = f"kb:content-data-facet-{self.generate_uuid()}"
        hash_id = f"kb:hash-{self.generate_uuid()}"

        file_entry = {
            "@id": file_entry_id,
            "@type": "uco-observable:File",
            "uco-core:hasFacet": [
                {
                    "@id": content_data_facet_id,
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:fileName": filename,
                    "uco-observable:filePath": filepath,
                    "uco-observable:sizeInBytes": size_in_bytes,
                    "uco-observable:observableCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": write_time
                    },
                    "uco-observable:hash": [
                        {
                            "@id": hash_id,
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA256"
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": sha256_hash
                            }
                        }
                    ]
                }
            ]
        }

        self.graph.append(file_entry)

    def serialize(self):
        data = {
            "@context": self.context,
            "@graph": self.graph
        }
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=4)

# Command-line interface for batch processing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CASE/UCO JSON-LD Generator')
    parser.add_argument('--input', type=str, required=True, help='Input data file')
    parser.add_argument('--batch_size', type=int, default=1000, help='Number of records to process in each batch')
    parser.add_argument('--output', type=str, default='case_output.jsonld', help='Output file')

    args = parser.parse_args()

    case_uco = CASEUCO(args.output)

    try:
        # Load input data from JSON file using ijson for efficient reading
        with open(args.input, 'r') as f:
            items = ijson.items(f, 'item')
            for item in items:
                try:
                    case_uco.add_file_system_entry(
                        filename=item['filename'],
                        filepath=item['filepath'],
                        write_time=item['write_time'],
                        sha256_hash=item['sha256_hash'],
                        size_in_bytes=item['size_in_bytes']
                    )
                except KeyError as e:
                    print(f"Missing key in item: {e}")
                except ijson.common.IncompleteJSONError as e:
                    print(f"JSON parsing error: {e}")

    except ijson.common.IncompleteJSONError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        case_uco.serialize()

    print(f"CASE/UCO JSON-LD dataHere's the updated `generate_input_data.py`, `internal_data_model.py`, and `uco_serialization.py` to incorporate the `size_in_bytes` attribute.

### Updated `generate_input_data.py`

```python
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
    size_in_bytes = random.randint(1, 1000)  # Generate random file size between 1 and 1000 bytes
    return {
        "filename": filename,
        "filepath": filepath,
        "write_time": write_time.isoformat(),
        "sha256_hash": sha256_hash,
        "size_in_bytes": size_in_bytes  # Include the generated file size
    }

# Generate 100000 file entries
data = [generate_file_entry(i) for i in range(100000)]

# Write the data to input_data.json
with open("input_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Generated 100000 file entries in input_data.json")




