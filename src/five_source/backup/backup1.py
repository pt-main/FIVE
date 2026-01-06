from modulefinder import test
import time
from templates import SPLIT_TOKEN, file
from zip import makeRlezip, readRlezip, unzipRlezip, RLE_SPLIT_BYTE
from diff_system import find_diff


RAWFILE = 'RAWFILE\x00'


def compile(raw: str, versions: dict[str, str], metadata: str = time.time()):
    result = ''
    # result += file(RAWFILE, raw, metadata)
    for version in versions.keys():
        data = versions[version]
        result += file(version, makeRlezip(data)[0].value, metadata)
        # result += file(version, find_diff(raw, data), metadata)
    return result

def decompile(five_file: str):
    versions = five_file.split(SPLIT_TOKEN)
    result = {}
    last_meta = False
    for file_version in versions[1:]:
        split = file_version.split('\n')
        version = split[0][:-1]
        metadata = split[1]
        file = '\n'.join(split[2:])
        file = unzipRlezip((file, RLE_SPLIT_BYTE))
        if last_meta:
            if last_meta != metadata: 
                print('Warning: data is invalid or defected')
        else:
            last_meta = metadata
        result[version] = file
    return result


def _decompile(five_file: str): # is not working 
    parsed = parse_compiled(five_file)
    RW = parsed[RAWFILE]
    result = {}
    for version in parsed.keys():
        if version != RAWFILE:
            content = parsed[version]
            reverse: str = content[::-1]
            diff_index = int(reverse[1:-1].split(',')[0])
            different = ','.join(reverse[1:-1].split(',')[1:])[::-1][1:-1]
            ver_data = RW[:diff_index]+different
            if len(RW) <= (diff_index + 1): 
                ver_data = RW[:diff_index]+different
            result[version] = ver_data
    return result




if __name__ == '__main__':
    example = {'test':'data1', 'test2':'data2'}
    compiled = compile('data11', example)
    print(compiled)
    decompiled = decompile(compiled)
    print(decompiled)
    print(example==decompiled)