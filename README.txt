## Install
1. Copy the 'ProfilerAssistant' folder into your Maya scripts folder
   (e.g. Documents/maya/<version>/scripts).

2. In the Script Editor (Python tab), run:

from ProfilerAssistant import main, profiler_recording, profiler_evaluation, ProfilerAssistant_ui

main.openWindow()


## Known limitations
- Reference contributors are limited to the top 3 events of the second recorded frame.
Events that only become significant in other frames may be missed.
Planned fix: restore the larger pool (top 10)or analyse all events across frames, since the data is already cached.

- Tested on a small number of scenes, only in Maya 2026
Results haven't been validated across a wide range of rigs, plugins or Maya versions.
Planned fix: further testing across maya versions, with problematic scenes I come across. Sharing tool with others to test.

- Prototype installation.
Manual copy into the scripts folder, no module or installer yet.