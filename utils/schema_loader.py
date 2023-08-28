import os
import json

def load_schema(schema_filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    schema_directory = os.path.join(script_directory, "..", "schemas")
    schema_path = os.path.join(schema_directory, schema_filename)

    with open(schema_path, "r") as f:
        schema = json.load(f)
    return schema
