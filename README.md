# UnityThings
Random Unity stuff

If you need CLI usage for a certain thing, just run it

## patch_graphics_api.py
Can be used to patch graphics APIs in `globalgamemanagers`, however this will break the game if it uses shaders, if you have a replacement shaders then you can use `patch_shader.py` to replace them

You also need to replace files in `GameName_Data/Resources` with ones that support your graphics APIs, you can create them by making an empty Unity project and building it with your graphics APIs

Available graphics APIs:
```
Direct3D11
OpenGLES2
OpenGLES3
OpenGLCore
Direct3D12
Vulkan
```

## patch_shader.py
Can be used to replace a shader by it's name

## list_shaders.py
Can be used to list all shaders used in a game

## dump_shaders_code.py
Can be used to dump all shaders source code used in a game

Note: Even though this tool is designed to dump shader source code, its not always gonna dump the source code, some platforms will have compiled shader binaries
