## Requirements
- Developed and tested on Maya 2026.
- Uses PySide6, so Maya 2025 or newer is expected. Not tested on other
  versions.
- matplotlib (used for the charts)

### Installing matplotlib
Run this in a terminal, using the `mayapy` that ships with your Maya:

**Windows**
```
"C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe" -m pip install matplotlib
```

**macOS**
```
/Applications/Autodesk/maya2026/Maya.app/Contents/bin/mayapy -m pip install matplotlib
```

**Linux**
```
/usr/autodesk/maya2026/bin/mayapy -m pip install matplotlib
```

Restart Maya afterwards. If you get a permissions error, run the terminal
as administrator or add `--user` to the command.

## Install
1. Copy the 'ProfilerAssistant' folder into your Maya scripts folder
   (e.g. Documents/maya/<version>/scripts or Documents/maya/scripts ).

2. Restart Maya afterwards

2. In the Script Editor (Python tab), run:

from ProfilerAssistant import main
main.openWindow()


## Known limitations

- Install is not user friendly
The tool is installed by copying the folder into Maya's scripts folder, and matplotlib has to be installed
separately through mayapy. There is no installer, shelf button or Maya module yet.
Planned fix: add a drag-and-drop installer 

- Reference contributors are limited to the top 3 events of the second recorded frame.
Events that only become significant in other frames may be missed.
Planned fix: restore the larger pool (top 10)or analyse all events across frames, since the data is already cached.

- Tested on a small number of scenes, only in Maya 2026
Results haven't been validated across a wide range of rigs, plugins or Maya versions.
Planned fix: further testing across maya versions, with problematic scenes I come across. Sharing tool with others to test.

- Prototype installation.
Manual copy into the scripts folder, no module or installer yet.

- Node name matching is incomplete.
In evaluation-bound scenes, node names are extracted from event descriptions with regex rules, but only 
for a fixed list of event types. Some results aren't valid scene nodes and are shown as "Not a selectable node".
Planned fix: replace the fixed list with pattern-based matching and test the rules against more scenes.

Side note: How render-bound scenes are handled
Render (VP Evaluation) events don't report which scene node they relate
to, so results are grouped by event name rather than by node. These
contributors can't be selected in the scene.


## Next steps
- drag-and-drop installer, including a shelf button and a check + auto install for matplotlib. (or ditching matplotlib?)
- Restore the larger pool of reference contributors (top 5? 10?)
- Replace the fixed event-type list with pattern-based node matching.
- Handle ties between evaluation- and render-bound results.
- Refactor duplicated interval-merging code into a shared helper.

- Bundle the txt files into 1 file for ease of use
- Save and select window opening in set project folder

- Research and implement guidence on how to speed up scene based on results
