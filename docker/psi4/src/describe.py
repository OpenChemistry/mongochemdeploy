import json
import os

def get_description():
    with open(os.path.join(os.path.dirname(__file__), 'description.json')) as f:
        return json.load(f)
