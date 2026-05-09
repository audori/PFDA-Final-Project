import maya.cmds as cmds

# Create ikHandle from selected joints

def create_con(ikh, end_jnt):
    # creates nurbs circle control
    ctrl_name = "arm_CON"
    con = cmds.circle(name=ctrl_name, nr=(1, 0, 0), r=2)[0]
    ctrl_grp = cmds.group(con, name=f"{ctrl_name}_GRP")

    temp_con = cmds.parentConstraint(end_jnt, ctrl_grp, maintainOffset=False)
    cmds.delete(temp_con)
   
    # Parent Ikh to con
    cmds.parent(ikh[0], con)

def add_locators(sel_jnts):
    for jnt in sel_jnts:
        # gets position of the joints and creates locators at their positions
        pos = cmds.xform(jnt, query=True, worldSpace=True, translation=True)
        loc = cmds.spaceLocator(name=f"{jnt}_LOC")
       
        cmds.xform(loc, worldSpace=True, translation=pos)
    pos_loc1 = cmds.xform('wrist_JNT_LOC', query=True, worldSpace=True, translation=True)
    pos_loc2 = cmds.xform('shoulder_JNT_LOC', query=True, worldSpace=True, translation=True)
   
    # Parent locators to con and jnt
    cmds.parent('shoulder_JNT_LOC', 'shoulder_JNT')
    cmds.parent('wrist_JNT_LOC', 'arm_CON')
   
    # add distance tool to measure distance between locators
    cmds.distanceDimension(sp=pos_loc1, ep=pos_loc2)
    cmds.rename('distanceDimension1', 'arm_ik_DIST')
   
def stretch_arm_nodes():
    length = cmds.getAttr('arm_ik_DIST' + '.distance')
    div_node = cmds.createNode('divide')
   
    cmds.connectAttr(length + '.distance', div_node + '.input1')
    cmds.setAttr(div_node + '.input2X', length)
   
    cmds.connectAttr(div_node + '.outputX', 'shoulder_JNT' + '.scaleX')
    cmds.connectAttr(div_node + '.outputX', 'elbow_JNT' + '.scaleX')
   
   
       
sel = cmds.ls(sl=True)

if len(sel) == 2:
    ik_han = cmds.ikHandle(name=f"{sel[1]}_IKH", solver='ikRPsolver')
    create_con(ik_han, sel[1])
    add_locators(sel)
    stretch_arm_nodes()
   
else:
    cmds.error('Please select 2 joints')