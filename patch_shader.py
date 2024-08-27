#!/usr/bin/python3

import os
import shutil
import argparse
import UnityPy

parser = argparse.ArgumentParser(
    prog="patch_shader.py",
    description="Unity shader patcher",
)
parser.add_argument("-d", "--game-data", required=True)
parser.add_argument("-s", "--single-file")
parser.add_argument("-b", "--shader-bundle", required=True)
parser.add_argument("-r", "--replacement-shader", required=True)
parser.add_argument("-t", "--target-shader", required=True)
args = parser.parse_args()

env = UnityPy.load(args.shader_bundle)
replacement_shader = None
available_replacement_shaders = []
for obj in env.objects:
    if obj.type.name == "Shader":
        shader = obj.read()
        available_replacement_shaders.append(f"  - {shader.m_ParsedForm.m_Name}")
        if shader.m_ParsedForm.m_Name == args.replacement_shader:
            replacement_shader = shader

if not replacement_shader:
    print(f"Could not find \"{args.replacement_shader}\" replacement shader")
    print("Available replacement shaders:\n" + "\n".join(available_replacement_shaders))
    exit()

allfiles = []
if args.single_file:
    allfiles.append(f"{args.game_data}/{args.single_file}")
else:
    allfiles.extend(f"{args.game_data}/{thing}" if os.path.isfile(f"{args.game_data}/{thing}") else None for thing in os.listdir(args.game_data))

for file in allfiles:
    patched = False
    env = UnityPy.load(file)
    for obj in env.objects:
        if obj.type.name == "Shader":
            shader = obj.read()
            if shader.m_ParsedForm.m_Name == args.target_shader:
                print(f"Patching {shader.m_ParsedForm.m_Name} in {file}")
                shader.set_raw_data(replacement_shader.get_raw_data())
                shader.save()
                patched = True

    if patched:
        with open(f"{file}_patched", "wb") as f:
            f.write(env.file.save())

        shutil.move(f"{file}_patched", file)
