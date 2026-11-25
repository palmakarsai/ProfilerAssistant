import maya.cmds as cmds
from pathlib import Path



def recordFrames(start_frame, end_frame, output_path, file_name):


    for frame in range(start_frame, end_frame + 1):
        # Start profiling
        cmds.profiler(sampling = True)

        # Switch frame
        cmds.currentTime(frame)

        # Refresh view - make sure to get full VP eval + show visually to user that multiple frames are being profiled
        cmds.refresh() ## Should I force?

        #Output result to txt
        cmds.profiler(output = Path(output_path) / f"{file_name}_frame_{frame:02d}_profiledata.txt")

        # Stop profiling
        cmds.profiler(sampling = False)

        #Reset profiler
        cmds.profiler(reset = True)

