import maya.cmds as cmds

# Create ikHandle from selected joints

def create_con(ikh, end_jnt):
    # cerates nurbs circle control
    ctrl_name = f"arm_CON"
    con = cmds.circle(name=ctrl_name, nr=(1, 0, 0), r=2)[0]
    ctrl_grp = cmds.group(con, name=f"{ctrl_name}_GRP")

    temp_con = cmds.parentConstraint(end_jnt, ctrl_grp, maintainOffset=False)
    cmds.delete(temp_con)

sel = cmds.ls(sl=True)

if len(sel) == 2:
    ik_han = cmds.ikHandle(name=f"{sel[1]}_IKH", solver='ikRPsolver')
    create_con(ik_han, sel[1])
   
else:
    cmds.error('Please select 2 joints')