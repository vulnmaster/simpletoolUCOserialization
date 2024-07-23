# generate_input_data.py
# written with the assistance of Generative AI

import json

# Function to generate a single example of email data
def generate_example(index):
    return {
        "email": f"example{index}@example.com",
        "byte_order": "Big-endian",
        "size_in_bytes": 17,
        "hash_method": "SHA256",
        "hash_value": "8fabebdaf41b54014f6c3507c44ae160547d05d31bd50d6a12234c5bc4bdb45c"
    }

# Generate 100,000 examples
data = [generate_example(i) for i in range(100000)]

# Write the data to input_data.json
with open("input_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Generated 10,000 examples in input_data.json")
