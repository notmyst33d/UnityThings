#!/usr/bin/python3

import enum
import argparse
import shutil
import UnityPy

# From Unity Reference Source Code
class GraphicsDeviceType(enum.Enum):
    Direct3D11 = 2
    OpenGLES2 = 8
    OpenGLES3 = 11
    OpenGLCore = 17
    Direct3D12 = 18
    Vulkan = 21

parser = argparse.ArgumentParser(
    prog="patch_graphics_apis.py",
    description="Unity graphics APIs patcher",
)
parser.add_argument("-d", "--game-data", required=True)
parser.add_argument("-a", "--graphics-apis", required=True)
args = parser.parse_args()

env = UnityPy.load(f"{args.game_data}/globalgamemanagers")
patched = False
for obj in env.objects:
    if obj.type.name == "BuildSettings":
        settings = obj.read()
        get_apis = lambda: [GraphicsDeviceType(api).name for api in settings.graphics_apis]
        print(f"Old Graphics APIs: {get_apis()}")
        settings.graphics_apis = [GraphicsDeviceType[api].value for api in args.graphics_apis.split(",")]
        print(f"New Graphics APIs: {get_apis()}")
        settings.save()
        patched = True

if not patched:
    print("Could not find BuildSettings for patching")
    exit()

with open(f"{args.game_data}/globalgamemanagers_patched", "wb") as f:
    f.write(env.file.save())

shutil.move(f"{args.game_data}/globalgamemanagers_patched", f"{args.game_data}/globalgamemanagers")