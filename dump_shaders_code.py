#!/usr/bin/python3

import os
import shutil
import argparse

import lz4
import UnityPy

class ShaderSubProgramEntry:
    def __init__(self, reader):
        self.offset = reader.read_int()
        self.length = reader.read_int()
        self.segment = reader.read_int()

class ShaderSubProgram:
    def __init__(self, reader):
        self.shader_version = reader.read_int()
        self.program_type = reader.read_int()
        reader.Position += 16
        self.keywords = reader.read_string_array()
        self.local_keywords = reader.read_string_array()
        self.program_code = reader.read_byte_array()

parser = argparse.ArgumentParser(
    prog="dump_shaders_code.py",
    description="Unity shader code dumper",
)
parser.add_argument("-d", "--game-data", required=True)
parser.add_argument("-r", "--recursive", default=False)
args = parser.parse_args()

allfiles = []
if args.recursive:
    for root, _, files in os.walk(args.game_data):
        allfiles.extend(allfiles.append(f"{root}/{file}") for file in files)
else:
    allfiles.extend(f"{args.game_data}/{thing}" if os.path.isfile(f"{args.game_data}/{thing}") else None for thing in os.listdir(args.game_data))

for file in allfiles:
    shaders = []
    env = UnityPy.load(file)
    for obj in env.objects:
        if obj.type.name == "Shader":
            shader = obj.read()
            data = lz4.block.decompress(shader.compressedBlob, uncompressed_size=shader.decompressedLengths[0])
            reader = UnityPy.streams.EndianBinaryReader(data, "<")
            entries = [ShaderSubProgramEntry(reader) for _ in range(0, reader.read_int())]
            subprograms = []
            index = 0
            for entry in entries:
                reader.Position = entry.offset
                subprograms.append(ShaderSubProgram(reader))

            for subprogram in subprograms:
                with open("dump/" + shader.m_ParsedForm.m_Name.replace("/", "_") + "_" + str(index) + ".shader", "wb") as f:
                    f.write(subprogram.program_code)
                index += 1
