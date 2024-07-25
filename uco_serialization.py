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
            "uco-observable": UCO_OBSERVABLE,
            "uco-types": UCO_TYPES,
            "uco-vocabulary": UCO_VOCABULARY,
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        }
        self.output_file = output_file
        self.init_output_file()
        self.first_object = True  # Track if it's the first object for proper JSON-LD formatting

    def init_output_file(self):
        with open(self.output_file, 'w') as f:
            f.write('[\n')

    def finalize_output_file(self):
        with open(self.output_file, 'a') as f:
            f.write('\n]')

    def generate_uuid(self):
        return str(uuid.uuid4())

    def add_file_system_entry(self, filename, filepath, write_time, sha256_hash):
        file_entry_id = f"{EX}file_entry-{self.generate_uuid()}"
        content_data_facet_id = f"{EX}content-data-facet-{self.generate_uuid()}"
        hash_id = f"{EX}hash-{self.generate_uuid()}"

        file_entry = {
            "@id": file_entry_id,
            "@type": f"{UCO_OBSERVABLE}File",
            f"{UCO_CORE}hasFacet": {
                "@id": content_data_facet_id,
                "@type": f"{UCO_OBSERVABLE}ContentDataFacet",
                f"{UCO_OBSERVABLE}fileName": {
                    "@type": "xsd:string",
                    "@value": filename
                },
                f"{UCO_OBSERVABLE}filePath": {
                    "@type": "xsd:string",
                    "@value": filepath
                },
                f"{UCO_OBSERVABLE}sizeInBytes": {
                    "@type": "xsd:integer",
                    "@value": "0"  # Size is not provided, set to 0 or calculate if needed
                },
                f"{UCO_OBSERVABLE}observableCreatedTime": {
                    "@type": "xsd:dateTime",
                    "@value": write_time
                },
                f"{UCO_OBSERVABLE}hash": {
                    "@id": hash_id,
                    "@type": f"{UCO_TYPES}Hash",
                    f"{UCO_TYPES}hashMethod": {
                        "@type": "vocabulary:HashNameVocab",
                        "@value": "SHA256"
                    },
                    f"{UCO_TYPES}hashValue": {
                        "@type": "xsd:hexBinary",
                        "@value": sha256_hash
                    }
                }
            }
        }

        self.serialize_object(file_entry)

    def serialize_object(self, obj):
        with open(self.output_file, 'a') as f:
            if not self.first_object:
                f.write(',\n')
            json.dump(obj, f, indent=4)
            self.first_object = False

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
            count = 0
            for item in items:
                try:
                    case_uco.add_file_system_entry(
                        filename=item['filename'],
                        filepath=item['filepath'],
                        write_time=item['write_time'],
                        sha256_hash=item['sha256_hash']
                    )
                    count += 1
                    if count % args.batch_size == 0:
                        # Evict memory and write current batch
                        case_uco.serialize_object(item)
                except KeyError as e:
                    print(f"Missing key in item: {e}")
                except ijson.common.IncompleteJSONError as e:
                    print(f"JSON parsing error: {e}")

    except ijson.common.IncompleteJSONError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Finalize the output file
        case_uco.finalize_output_file()

    print(f"CASE/UCO JSON-LD data has been written to {args.output}")

