import uuid
import rdflib
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, XSD
import json
import argparse
import os

from internal_data_model import InternalEmail, InternalRelationship

UCO_CORE = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/core/")
UCO_OBSERVABLE = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/observable/")
UCO_TYPES = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/types/")
UCO_VOCABULARY = rdflib.Namespace("https://ontology.unifiedcyberontology.org/uco/vocabulary/")
EX = rdflib.Namespace("http://example.org/kb/")

class CASEUCO:
    def __init__(self):
        self.context = {
            "@vocab": "http://example.org/local#",
            "kb": "http://example.org/kb/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        }
        self.graph = Graph()
        self.graph.bind("uco-core", UCO_CORE)
        self.graph.bind("uco-observable", UCO_OBSERVABLE)
        self.graph.bind("uco-types", UCO_TYPES)
        self.graph.bind("uco-vocabulary", UCO_VOCABULARY)
        self.graph.bind("ex", EX)

    def generate_uuid(self):
        return str(uuid.uuid4())

    def add_email_address(self, email, byte_order="Big-endian", size_in_bytes=17, hash_method="SHA256", hash_value=""):
        email_address_id = EX[f"extracted_email_address-{self.generate_uuid()}"]
        content_data_facet_id = EX[f"content-data-facet-{self.generate_uuid()}"]
        hash_id = EX[f"hash-{self.generate_uuid()}"]

        self.graph.add((email_address_id, RDF.type, UCO_OBSERVABLE.EmailAddress))
        
        content_data_facet = BNode()
        self.graph.add((content_data_facet, RDF.type, UCO_OBSERVABLE.ContentDataFacet))
        self.graph.add((content_data_facet, UCO_OBSERVABLE.byteOrder, Literal(byte_order, datatype=UCO_VOCABULARY.EndiannessTypeVocab)))
        self.graph.add((content_data_facet, UCO_OBSERVABLE.sizeInBytes, Literal(size_in_bytes, datatype=XSD.integer)))
        self.graph.add((content_data_facet, UCO_OBSERVABLE.dataPayload, Literal(email)))
        
        email_hash = BNode()
        self.graph.add((email_hash, RDF.type, UCO_TYPES.Hash))
        self.graph.add((email_hash, UCO_TYPES.hashMethod, Literal(hash_method, datatype=UCO_VOCABULARY.HashNameVocab)))
        self.graph.add((email_hash, UCO_TYPES.hashValue, Literal(hash_value, datatype=XSD.hexBinary)))
        self.graph.add((content_data_facet, UCO_OBSERVABLE.hash, email_hash))
        
        self.graph.add((email_address_id, UCO_CORE.hasFacet, content_data_facet))
        return email_address_id

    def add_relationship(self, source_id, target_id, relationship_type="Contained_Within", range_offset=0, range_size=0):
        relationship_id = EX[f"relationship-{self.generate_uuid()}"]

        self.graph.add((relationship_id, RDF.type, UCO_OBSERVABLE.ObservableRelationship))
        self.graph.add((relationship_id, UCO_CORE.source, URIRef(source_id)))
        self.graph.add((relationship_id, UCO_CORE.target, URIRef(target_id)))
        self.graph.add((relationship_id, UCO_CORE.kindOfRelationship, Literal(relationship_type)))
        self.graph.add((relationship_id, UCO_CORE.isDirectional, Literal(True, datatype=XSD.boolean)))
        
        data_range_facet = BNode()
        self.graph.add((data_range_facet, RDF.type, UCO_OBSERVABLE.DataRangeFacet))
        self.graph.add((data_range_facet, UCO_OBSERVABLE.rangeOffset, Literal(range_offset, datatype=XSD.integer)))
        self.graph.add((data_range_facet, UCO_OBSERVABLE.rangeSize, Literal(range_size, datatype=XSD.integer)))
        
        self.graph.add((relationship_id, UCO_CORE.hasFacet, data_range_facet))
        return relationship_id

    def serialize_graph(self, output_file, format='json-ld'):
        with open(output_file, 'ab') as f:
            f.write(self.graph.serialize(format=format).encode('utf-8'))
        self.graph = Graph()  # Reset the graph to free memory

# Command-line interface for batch processing
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='CASE/UCO JSON-LD Generator')
        parser.add_argument('--input', type=str, required=True, help='Input data file')
        parser.add_argument('--batch_size', type=int, default=1000, help='Number of records to process in each batch')
        parser.add_argument('--output', type=str, default='case_output.jsonld', help='Output file')

        args = parser.parse_args()

        case_uco = CASEUCO()

        # Load input data from JSON file
        with open(args.input, 'r') as f:
            input_data = json.load(f)

        # Convert input data to InternalEmail objects
        emails = [
            InternalEmail(
                email=item['email'],
                byte_order=item['byte_order'],
                size_in_bytes=item['size_in_bytes'],
                hash_method=item['hash_method'],
                hash_value=item['hash_value']
            ) for item in input_data
        ]

        # Process data in batches
        for i in range(0, len(emails), args.batch_size):
            batch = emails[i:i + args.batch_size]
            for record in batch:
                case_uco.add_email_address(
                    email=record.email,
                    byte_order=record.byte_order,
                    size_in_bytes=record.size_in_bytes,
                    hash_method=record.hash_method,
                    hash_value=record.hash_value
                )
            
            # Serialize and write the current batch to the output file
            case_uco.serialize_graph(args.output)

        print(f"CASE/UCO JSON-LD data has been written to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")
