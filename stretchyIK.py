# Create ikHandle from selected joints
# Copy past the code into the python maya script editor for this to work!

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
    cmds.parent('shoulder_JNT_LOC', 'clav_CON')
    cmds.parent('wrist_JNT_LOC', 'arm_CON')
   
    # Set locators invisible
    cmds.setAttr('shoulder_JNT_LOC.visibility', 0)
    cmds.setAttr('wrist_JNT_LOC.visibility', 0)
   
    # add distance tool to measure distance between locators
    cmds.distanceDimension(sp=pos_loc1, ep=pos_loc2)
    cmds.rename('distanceDimension1', 'arm_ik_DIST')
    cmds.setAttr('arm_ik_DIST.visibility', 0)
   
def stretch_squash_arm_nodes():
    # Calculate and stretch arm to wherever you move the wrist con  
    length = cmds.getAttr('arm_ik_DIST.distance')
    div_node = cmds.createNode('multiplyDivide')
    cmds.setAttr(div_node + '.operation', 2)
   
    cmds.connectAttr('arm_ik_DIST.distance', div_node + '.input1X')
    cmds.setAttr(div_node + '.input2X', length)
   
    clamp_node = cmds.createNode('clamp')
    cmds.setAttr(clamp_node + '.minR', 1)
    cmds.setAttr(clamp_node + '.maxR', 10)
   
    cmds.connectAttr(div_node + '.outputX', clamp_node + '.inputR')
   
    cmds.connectAttr(clamp_node + '.outputR', 'shoulder_JNT.scaleX')
    cmds.connectAttr(clamp_node + '.outputR', 'elbow_JNT.scaleX')
   
    # Squash
    div_exp_node = cmds.createNode('multiplyDivide')
    cmds.setAttr(div_exp_node + '.operation', 3)
    cmds.setAttr(div_exp_node + '.input2X', .5)
   
    cmds.connectAttr(clamp_node + '.outputR', div_exp_node + '.input1X')
   
    divide = cmds.createNode('multiplyDivide')
    cmds.setAttr(divide + '.operation', 2)
    cmds.setAttr(divide + '.input1X', 1)
   
    cmds.connectAttr(div_exp_node + '.outputX', divide + '.input2X')
   
    cmds.connectAttr(divide + '.outputX', 'shoulder_JNT.scaleY')
    cmds.connectAttr(divide + '.outputX', 'shoulder_JNT.scaleZ')
   
    cmds.connectAttr(divide + '.outputX', 'elbow_JNT.scaleY')
    cmds.connectAttr(divide + '.outputX', 'elbow_JNT.scaleZ')

sel = cmds.ls(sl=True)

if len(sel) == 2:
    # Create IKH and make it invisible
    ik_han = cmds.ikHandle(name=f"{sel[1]}_IKH", solver='ikRPsolver')
    cmds.setAttr('wrist_JNT_IKH.visibility', 0)
    create_con(ik_han, sel[1])
    add_locators(sel)
    stretch_squash_arm_nodes()
     
else:
    cmds.error('Please select 2 joints')