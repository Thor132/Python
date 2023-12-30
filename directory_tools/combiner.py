import argparse
import ctypes
import os
import json
import glob
import platform
import sys
import time

#
def load_file_data(path):
    output = {}
    for path in ["{0}/**/*.json".format(path)]:
        files = glob.glob(path, recursive=True)
        for file in files:
            if os.path.isfile(file):
                with open(file) as f:
                    data = json.load(f)
                    if data:
                        key = os.path.basename(file)
                        print("Loaded {0}".format(key))
                        output[key] = data
    return output  
#
def consolidate_file_dict(input):
    byFilename = {}
    byPath = {}

    for key, value in input.items():
        for file in value["files"]:
            if len(file["file"]) > 0 and file["file"][0].startswith("#"):
                continue
        
            filename = file["file"][len(file["file"]) - 1]
            fullFilename = os.path.join(*file["file"])

            file["filenames"] = { "filename": filename, "fullFilename": fullFilename }
            file["source"] = { "key": key, "source": value["source"] }

            if filename not in byFilename:
                byFilename[filename] = []
            byFilename[filename].append(file)

            if fullFilename not in byPath:
                byPath[fullFilename] = [] 
            byPath[fullFilename].append(file)
            

    return (dict(sorted(byFilename.items())), dict(sorted(byPath.items())))
#
def find_possible_duplicates(input):
    output = {}
    for key, value in input.items():
        if len(value) > 1:
            output[key] = value
    return output
#
def write_compact_json_file(filename, source_name, source_list, input):
    cnt = 0
    with open("{0}".format(filename), 'w') as output:
        output.write("{{ \"time\": {0}, \"{1}\": {2}, \"files\": [\n".format(int(time.time()), source_name, json.dumps(source_list)))

        for key, value in input.items():
            if len(value) == 1:
                info = value[0]
                if "filenames" in info:
                    del info["filenames"]
                if "source" in info:
                    del info["source"]
                output.write('{0}{1}'.format(",\n" if cnt > 0 else "", json.dumps(info)))
                cnt += 1
            else:
                print("WARNING! {0} has more than one entry".format(key))
                #TODO: Except?
        output.write("\n] }")
#
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', dest='dir', required=True)
    args = parser.parse_args()

    allFiles = load_file_data(args.dir)
    (dirFiles, dirPaths) = consolidate_file_dict(allFiles)

    dupes = {}
    dupes["file"] = find_possible_duplicates(dirFiles)
    dupes["path"] = find_possible_duplicates(dirPaths)

    with open("output/{0}_dups.json".format(args.dir), "w") as outfile: 
        outfile.write(json.dumps(dupes, indent = 4))

    write_compact_json_file("output/{0}.json".format(args.dir), args.dir, list(allFiles.keys()), dirPaths)
