# internal_data_model.py

class InternalEmail:
    def __init__(self, email, byte_order, size_in_bytes, hash_method, hash_value):
        self.email = email
        self.byte_order = byte_order
        self.size_in_bytes = size_in_bytes
        self.hash_method = hash_method
        self.hash_value = hash_value

class InternalRelationship:
    def __init__(self, source_id, target_id, relationship_type, range_offset, range_size):
        self.source_id = source_id
        self.target_id = target_id
        self.relationship_type = relationship_type
        self.range_offset = range_offset
        self.range_size = range_size
