
=======================================
Program to infer schema from JSON file
========================================


Simple tool to infer JSON schemas


Features
--------

* Inferring schema from single sample



Example of using the program to generate a schema from a list of samples::

    $ cat samples.json
    {"name": "Claudio", "age": 29}
    {"name": "Roberto", "surname": "Gomez", "age": 72}

    $ python JsonSchema/main.py samples.json
    {
    "type": "array",
    "properties": {
        "age": {
        "required": false,
        "tag": "",
        "description": "",
        "type": "integer"
        },
        "name": {
        "required": false,
        "tag": "",
        "description": "",
        "type": "string"
        },
        "surname": {
        "required": false,
        "tag": "",
        "description": "",
        "type": "string"
        }
    }
    }

Run with 

```git remote add origin https://github.com/Sensei-akin/JsonSchema.git```
