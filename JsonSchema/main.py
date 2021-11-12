import argparse,json,sys,os

from jsonschema import jsonschema

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Json schema inferencer')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    infile    = args.infile.read()
    file_name = args.infile.name
    
    js=jsonschema()
    data = js.guess_schema(json.loads(infile))['properties']['message']['properties']
    output_name = os.path.splitext(f"{file_name}")[0].split('/')[2]+'_schema.json'
    with open(f'schema/{output_name}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    