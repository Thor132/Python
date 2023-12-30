import argparse
import ctypes
import os
import json
import glob
import platform
import time

#
def get_free_space(dirname):
    """Return folder/drive free space."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize
#
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', dest='pattern', default='*')
    parser.add_argument('-s', '--s', dest='source')
    args = parser.parse_args()

    source = ""
    output_file = "out.json"
    if args.source:
        source = args.source
        output_file = "{0}.json".format(source)

    recordedFiles = {}

    path = "{0}/**/*".format(args.pattern)
    files = glob.glob(path, recursive=True)
    for file in files:
        if os.path.isfile(file):
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)                  
            file_dir = file.split(os.sep)

            info = { "file": file_dir, "size": size, "mtime": mtime }
            recordedFiles[file] = info

    # Not just dumping to json at end since I want a specific file format
    with open("{0}".format(output_file), 'w') as output:
        free_b = get_free_space(".")
        free_gb = free_b / 1024 / 1024 / 1024
        free_tb = free_gb / 1024
        output.write("{{ \"time\": {0}, \"source\": \"{1}\", \"free\": {2}, \"gb_free\": {3:.2f}, \"tb_free\": {4:.2f}, \"files\": [\n".format(int(time.time()), source, free_b, free_gb, free_tb))

        cnt = 0
        for key, value in dict(sorted(recordedFiles.items())).items():
            output.write('{0}{1}'.format(",\n" if cnt > 0 else "", json.dumps(value)))
            cnt += 1

        output.write("\n] }")
