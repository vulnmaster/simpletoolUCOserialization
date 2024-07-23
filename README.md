# Problem

**CASE/UCO adopters need to serialize outputs from command line tools into `.jsonld`.** In our use case, adopters are not able to run any database (e.g., graph database) as part of the technology stack and the computer running this program is a typical business laptop with ~8GB of memory. In this example, we have a notional software tool's json-formatted output of a list of email addresses and properties. We need to convert this data of 100K records into UCO-compliant `.jsonld`. We have included the data generation script `generate_input_data.py` to help you generate the 100K records. 

This project serves as a working example that presents a simple mapping of a local data model to the Unified Cyber Ontology, and a batch serializer for processing json records.

## Solution

To handle large datasets efficiently and prevent memory issues, you can use several strategies:

- **Batch Processing**: Process and serialize data in smaller batches rather than loading all data into memory at once.
- **Streaming**: Use streaming techniques to handle large data sets incrementally.
- **Efficient Data Structures**: Ensure that your data structures and serialization methods are optimized for memory usage.
- **Garbage Collection**: Explicitly trigger garbage collection to free up unused memory.

### Approach

Here's an enhanced approach using batch processing and streaming to manage memory usage efficiently. We'll process the data in chunks and write each chunk to the output file incrementally.

### Instructions

1. **Modify the `CASEUCO` Class**: Modify the `CASEUCO` class in `uco_serialization.py` to support batch processing and incremental writing of the `.jsonld` output.

2. **Explanation**:
    - **Batch Processing**: The input data is processed in batches defined by `batch_size`.
    - **Graph Reset**: After each batch is serialized and written to the output file, the RDF graph is reset to free up memory.
    - **Incremental Writing**: The `serialize_graph` function appends each batch's serialized data to the output file.

### Usage

1. **Save the Code**: Save the altered `CASEUCO` code to a file named `uco_serialization.py`.
2. **Simulate Input Data**: Simulate an input data file with records to be processed in batches. For example, you can generate `input_data.json` using the `generate_input_data.py` script.
3. **Run the Script**: Run the script from the command line:

    ```sh
    python uco_serialization.py --input input_data.json --batch_size 1000 --output case_output.jsonld
    ```

### Example Scripts

#### `generate_input_data.py`

This script generates a JSON file (`input_data.json`) with 100,000 examples of email addresses and their corresponding data.

#### `uco_serialization.py`

This script processes the input data in batches and serializes the output to a .jsonld file.