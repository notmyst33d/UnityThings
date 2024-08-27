#!/usr/bin/python3

import os
import shutil
import argparse
import UnityPy

parser = argparse.ArgumentParser(
    prog="list_shaders.py",
    description="Unity shader listing",
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
            shaders.append(f"  - {shader.m_ParsedForm.m_Name}")

    if len(shaders) != 0:
        print(file + ":\n" + "\n".join(shaders))
