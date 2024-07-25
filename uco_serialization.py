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

    def add_file_system_entry(self, filename, filepath, write_time, sha256_hash):
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
                    "uco-observable:sizeInBytes": 0,  # Size is not provided, set to 0 or calculate if needed
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
                        sha256_hash=item['sha256_hash']
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

    print(f"CASE/UCO JSON-LD data has been written to {args.output}")


