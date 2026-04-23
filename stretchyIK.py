import maya.cmds as cmds

# Create ikHandle from selected joints

sel = cmds.ls(sl=True)

if len(sel) == 2:
    ik_han = cmds.ikHandle()
else:
    cmds.error('Please select 2 joints')