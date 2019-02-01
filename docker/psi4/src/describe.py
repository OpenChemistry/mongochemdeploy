def get_description():
    return {
        "name": "PSI4",
        "version": "1.2.1",
        "input": {
            "format": "xyz",
            "parameters": {
                "theory": {
                    "type": "string",
                    "description": "The theory level: ks | hf",
                    "default": "hf"
                },
                "task": {
                    "type": "string",
                    "description": "The calculation task: energy | optimize | frequency",
                    "default": "energy"
                },
                "basis": {
                    "type": "string",
                    "description": "The basis set.",
                    "default": "cc-pvdz"
                },
                "functional": {
                    "type": "string",
                    "description": "The XC functional (if ks theory).",
                    "default": "b3lyp"
                },
                "charge": {
                    "type": "number",
                    "description": "The net charge of the system.",
                    "default": 0
                },
                "multiplicity": {
                    "type": "number",
                    "description": "The spin multiplicity.",
                    "default": 1
                }
            }
        },
        "output": {
            "format": "cjson"
        }
    }