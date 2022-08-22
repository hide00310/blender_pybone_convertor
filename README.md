# blender_pybone_convertor
Blender addon for converting bones using the user defined python script.

## Features
+ Rename bones using the user defined python script
+ Convert data of bones by comparing the target and source armature
  + e.g. align the roll of bones to the source armature

## Installation
1. Download the code from main in zip format
1. Install in Blender
   1. Edit > Preferences > Add-ons
     1. Click install button
     1. Select downloaded zip
     1. Enable the addon
1. The addon can be found in 3D View > Right side panel > Misc > PyBone Convertor

## Usage
### Rename bones
1. Create a python script to rename a bone
   + Define a "rename(context, bone_name)" function that returns a renamed bone name
   + e.g. [sample.py](./presets/sample.py)
1. Set the script path to the "Script" property
   + "${.}" will resolve to "this_addon_file_directory/presets"
   + e.g. "${.}/sample.py" will resolve to the path of [sample.py](./presets/sample.py)
1. Select target armature
1. Click "Convert" button

#### Presets
There are preset scripts in [preset directory](./presets).

##### [sample.py](./presets/sample.py)
A sample script that adds the string "prefix:" to name of bones.

##### [unity_to_mixamo.py](./presets/unity_to_mixamo.py)/[mixamo_to_unity.py](./presets/mixamo_to_unity.py)
A script that rename the bone of unity name to/from the mixamo name.

I created this script for the Mixamo add-on for Blender.
The procedures is described in [Convert Unity bones for Mixamo add-on for Blender](#Convert-Unity-bones-for-Mixamo-add-on-for-Blender).

This script logic is based on
    https://github.com/MinaPecheux/BlenderPlugins/blob/master/Rigging/MixamoRigRenamer.py

### Source Armature
If the "Source Armature" property is set, 
the following conversions are available.

+ Align the roll of bones to the Source Armature
+ Add bones that exist in the Source Armature but not in the target armature
+ Remove bones that exist in the target armature but not in the Source Armature
+ Change the bones to the layers. The bones exist in the target armature but not in the Source Armature

Note : the conversions are executed after renaming.

### Convert Unity bones for Mixamo add-on for Blender
To use the [Mixamo add-on for Blender](https://substance3d.adobe.com/plugins/mixamo-in-blender/) for the model set up for Unity, follow these procedures.

1. Download the Mixamo model by fbx
1. Import the Mixamo model by blender
1. Select armature of the Unity model
1. Convert by these settings
   + Script : ${.}/unity_to_mixamo.py
   + Source Armature : the Mixamo model
   + Align Roll : Check
   + Add not existing bones : Check
1. "Create Control Rig" in "Mixamo add-on for Blender" can be executed
