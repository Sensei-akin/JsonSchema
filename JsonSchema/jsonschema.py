import argparse
import json, sys,os
class jsonschema():
    TYPES = {
    type(1): 'integer',
    type(1.2): 'number',
    type("abc"): 'string',
    type(u"abc"): 'string',
    type(True): 'boolean',
    type([]): 'enum',
    type(()): 'array',
    type({}): 'array',
    type(None): 'null',
    }

    COMPOUND_TYPES = frozenset(['array', 'enum'])
    SCALARS_TYPES = set(TYPES.values()) - COMPOUND_TYPES
    
    def parse_sample(self,item, paths=None, base=None):
        base = base or ()
        paths = paths or {}  # path container and counters
        paths.setdefault(base, 0)
        paths[base] += 1
        type_ = self.TYPES.get(type(item), "any")
        base1 = base + (type_,)
        paths.setdefault(base1, 0)
        if type_ in self.SCALARS_TYPES:
            paths[base1] += 1
        elif type_ == "enum":
            paths[base1] += 1
            base1b = base1 + (None,)  # adding extra place for possible extensions (eg array index)
            paths.setdefault(base1b, 0)
            for subitem in item:
                self.parse_sample(subitem, paths=paths, base=base1b)
        elif type_ == "array":
            paths[base1] += 1
            for (k, subitem) in item.items():
                base1b = base1 + (k,)
                self.parse_sample(subitem, paths=paths, base=base1b)

        return paths


    def find_type(self,schema, typename):
        for t in schema["type"]:
            if isinstance(t, dict) and t.get("type") == typename:
                return t
        return None


    def build_element(self,paths, schema, path, pos=0):
        if pos >= len(path):
            return
        typename = path[pos]
        if typename in self.SCALARS_TYPES:
            if "type" in schema:
                if schema["type"] != typename:
                    if isinstance(schema["type"], list):
                        if typename in schema["type"]:
                            return
                        schema["type"].append(typename)
                        

                    else:
                        schema["type"] = [schema["type"], typename]
            
            else:
                schema["type"] = typename
                # scalar type is always a leaf. No need to call.
                # build_element(paths, schema, path, pos+1)
        elif typename == "array":
            if "type" in schema:
                if schema["type"] != typename:
                    typename='array'
                    if isinstance(schema["type"], list):
                        typedef = find_type(schema, "array")
                        if typedef is None:
                            typedef = {"type": "array", "properties": {}}
                            schema["type"].append(typedef)
                    else:
                        typedef = {"type": "array", "properties": {}}
                        schema["type"] = [schema["type"], typedef]
                    props = typedef["properties"]
                else:
                    props = schema["properties"]
            else:
                schema["type"] = typename
                props = schema["properties"] = {}
            # deal with properties
            if pos + 1 < len(path):
                propname = path[pos + 1]
                if propname in props:
                    subschema = props[propname]
                else:
                    subschema = props[propname] = {
                        "required": False,'tag' : "",'description':""
                        # property less frequent than base object
                    }
                self.build_element(paths, subschema, path, pos + 2)
        elif typename == "enum":
            if "type" in schema:
                if schema["type"] != typename:
                    if isinstance(schema["type"], list):
                        typedef = find_type(schema, "array")
                        if typedef is None:
                            typedef = {"type": "array", "items": {}}
                            schema["type"].append(typedef)
                    else:
                        typedef = {"type": "array", "items": {}}
                        schema["type"] = [schema["type"], typedef]
                    items = typedef["items"]
                else:
                    items = schema["items"]
            else:
                schema["type"] = typename
                items = schema["items"] = {}  # schema
            # deal with items
            if pos + 1 < len(path):
                assert path[pos + 1] is None  # for now
                subschema = items
                self.build_element(paths, subschema, path, pos + 2)


    def build_schema(self,paths):
        schema = {}
        for path in sorted(paths.keys()):
            self.build_element(paths, schema, path)

        return schema


    def guess_schema(self,s):
        paths = self.parse_sample(s)
        return self.build_schema(paths)


    
    