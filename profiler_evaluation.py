from functools import total_ordering

import maya.cmds as cmds
import re
from pathlib import Path

#def read_recorded_frame(frame):
    #cmds.profiler(load = Path(output_path) / f"{file_name}_frame_{frame}_profiledata.txt")

def get_event_count():
    event_count = cmds.profiler(query=True, eventCount=True)
    return event_count

def build_category_cache(recorded_frames):
    cmds.profiler(load=recorded_frames[0])
    category_names = cmds.profiler(query=True, allCategories=True)
    return {i: name for i, name in enumerate(category_names)}

def collect_events_info(event_count,category_cache, mode):
    events = []

    # Query event name and duration for each event
    for idx in range(event_count):

        event_name = None
        category_idx = None
        event_description = None

        duration = cmds.profiler(query=True, eventDuration=True, eventIndex=idx)
        start_time = cmds.profiler(query=True, eventStartTime=True, eventIndex=idx)

        if mode == "event":
            event_name = cmds.profiler(query=True, eventName=True, eventIndex=idx)
        elif mode == "category":
            category_idx = cmds.profiler(query=True, eventCategory=True, eventIndex=idx)
        elif mode == "all":
            event_description = cmds.profiler(query=True, eventDescription=True, eventIndex=idx)
            event_name = cmds.profiler(query=True, eventName=True, eventIndex=idx)
            category_idx = cmds.profiler(query=True, eventCategory=True, eventIndex=idx)
        else:
            raise ValueError(f"Invalid mode: '{mode}'. Expected 'event', 'category' or 'all'")

        events.append({
            "event_name": event_name,
            "duration": duration,
            "category": category_cache[category_idx] if category_idx is not None else None,
            "start_time": start_time,
            "description": event_description
        })

    return events

def event_duration_sum(events):
    eval_intervals = {}
    render_intervals = {}

    grouped_eval_events = {}
    grouped_render_events = {}

    for item in events:
        name = item["event_name"]
        interval = (item["start_time"], item["start_time"] + item["duration"])

        if item["category"] == "Evaluation":
            eval_intervals.setdefault(name, []).append(interval)
        elif item["category"] == "VP Evaluation":
            render_intervals.setdefault(name, []).append(interval)

    for name, intervals in eval_intervals.items():
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]
        for start, end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))

        duration = sum(end - start for start, end in merged)
        grouped_eval_events[name] = duration

    for name, intervals in render_intervals.items():
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]
        for start, end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]
            if start <= last_end:
                merged[-1] = (last_start, max(last_end, end))
            else:
                merged.append((start, end))

        duration = sum(end - start for start, end in merged)
        grouped_render_events[name] = duration

    grouped_events = {**grouped_eval_events, **grouped_render_events}

    return grouped_events


# TODO: extract merging logic into helper function

def category_duration_sum(events, category_name):
    intervals = [
        (e["start_time"], e["start_time"] + e["duration"])
        for e in events
        if e["category"] == category_name
    ]
    if not intervals:
        return 0.0

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return sum(end - start for start, end in merged)

def extract_object(description):
    # Case 1: CustomEvaluatorLayer — extract just the node inside the brackets
    # e.g. "deformer|CustomEvaluatorLayer[1,Deer_rig:deer_skn]" -> "Deer_rig:deer_skn"
    bracket_match = re.search(r'\[[\d]+,([\w:]+)\]', description)
    if bracket_match:
        return bracket_match.group(1)

    # Case 2: Full namespaced path — keep as-is, it's already selectable
    # e.g. "DeerLieDown_pose_01:Deer_rig_102:rArmFunctionShape"
    # e.g. "fawn_creature_rg_001:wrap2"
    namespace_match = re.search(r'[\w]+(?::[\w]+)+', description)
    if namespace_match:
        return namespace_match.group(0)

    # Case 3: "Compute - NodeName" or "EvaluateNode - NodeName"
    dash_match = re.search(r'\s-\s([\w]+)', description)
    if dash_match:
        return dash_match.group(1)

    # Case 4: Fallback
    first_word = description.split()[0] if description else "unknown"
    return first_word.split('|')[-1]

def sum_eval_events_by_node(events):
    # Group events on same nodes and add their duration
    grouped_events = {}

    default_categories = [
        "EvaluateNode",
        "Compute",
        "NodePreEvaluation",
        "CustomEvaluateCluster",
        "EvaluateNodesInTransparentCluster",
        "NodeExternalDataDirty",
        "GPUOverrideChainEval",
        "NodePostEvaluationIndirect",
        "MPxGPUDeformerEvaluate",
        "GPUOverrideMeshEval",
        "GPUOverrideMeshEnqueueKernels",
        "SkipAll",
        "readbackGPU",
        "updateGPU",
        "GPUOverrideMeshGenerateBoundingBox",
        "GPUOverrideMeshUpdateGeometryMatrix",
        "GPUOverrideMeshApplyTweaks",
        "NodePostEvaluationLeaveDirty",
        "GPUOverrideMeshAcquireSharedVp2Buffers",
        "GPUOverrideMeshUpdateVp2Matrix",
        "GPUOverrideMeshReleaseSharedVp2Buffers",
    ]

    for item in events:
        if item["category"] == "Evaluation":
            if item["description"] is not None and item["event_name"] in default_categories:
                # Group by node names and add durations for each group
                event_name = extract_object(item["description"])
            else:
                event_name = item["event_name"]
            duration = item["duration"]
            grouped_events[event_name] = grouped_events.get(event_name, 0) + duration

    return grouped_events


def get_top_n_event_names(event_list,top_num):
    # Add top contributors to their correlating list
    sorted_event_list = sorted(event_list.items(), key=lambda x: x[1], reverse=True)
    top_events = sorted_event_list[:top_num]
    top_event_names = [event[0] for event in top_events]
    return top_event_names

def get_median(data):
    if not data:
        return None

    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2

    if n % 2 == 0:
        # For even length: average of the two middle elements
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        # For odd length: the middle element
        return sorted_data[mid]

def get_bound_type(recorded_frames, category_cache,  progress_callback=None):

    total_steps = len(recorded_frames) * 2

    #  create list for bound-types
    bound_type_list = []

    if not recorded_frames:
        print("Recorded frames was empty")
        return None

    for idx, i in enumerate(recorded_frames):
        #Read txt file
        cmds.profiler(load = i)
        #Collect all events info  and put them in a list of dicts
        events = collect_events_info(get_event_count(), category_cache, mode="category")

        evaluation_time = category_duration_sum(events, "Evaluation")
        render_time = category_duration_sum(events, "VP Evaluation")

        print(f"eval time: {evaluation_time:.2f}")
        print(f"render time: {render_time:.2f}")

        bound_type_list.append("EB" if evaluation_time > render_time else "RB")

        if progress_callback:
            progress_callback(int((idx + 1) / total_steps * 100))


    # Get bound_type across frames
    EB_count = bound_type_list.count("EB")
    RB_count = bound_type_list.count("RB")

    # TODO: handle ties - currently defaults to RB
    if EB_count > RB_count:
        bound_type = "EB"
    else:
        bound_type = "RB"

    return bound_type, evaluation_time, render_time



def load_and_collect(filepath, category_cache):
    # Load profile file and return all needed info
    cmds.profiler(load=filepath)
    return collect_events_info(get_event_count(), category_cache, mode="all")

def execute_profiling(recorded_frames, top_num,progress_callback=None):
    category_cache = build_category_cache(recorded_frames)

    #Load each file once - cache the parsed events
    all_frames_events = []
    total= len(recorded_frames)
    for idx, frame_path in enumerate(recorded_frames):
        event= load_and_collect(frame_path, category_cache)
        all_frames_events.append(event)

    # Get bound type - from cache
    bound_type, eval_time, render_time = get_bound_type(all_frames_events)

    # Reference frame - from cache
    ref_events = all_frames_events[1]
    if bound_type == "EB":
        ref_grouped = sum_eval_events_by_node(ref_events)
    else:
        ref_grouped = event_duration_sum(ref_events)

    top_event_names = get_top_n_event_names(ref_grouped, top_num)

    # Process all frames - from cache
    top_event_grp = {name: [] for name in top_event_names}
    for idx, events in enumerate(all_frames_events):
        final_sum = (sum_eval_events_by_node(events)
                     if bound_type == "EB"
                     else event_duration_sum(events)
                     )
        for name, dur in final_sum.items():
            if name in top_event_grp:
                top_event_grp[name].append(dur)

    #Get median of each event and store with event name
    top_contributors = []
    for event_name, durations in top_event_grp.items():
        top_contributors.append({
            "event_name": event_name,
            "median_duration": get_median(durations)
        })

    #Sort by duration again to get top contributor event-duration pairs
    valid = [x for x in top_contributors if x["median_duration"] is not None]
    invalid = [x for x in top_contributors if x["median_duration"] is None]

    valid.sort(key=lambda x: x["median_duration"], reverse=True)
    top_contributors_ranked = valid + invalid # force None to be at the end


     # Convert ticks to milliseconds
    TICKS_TO_MS = 1 / 1000.0
    for contributor in top_contributors_ranked:
        if contributor["median_duration"] is not None:
            contributor["median_duration"] = contributor["median_duration"] * TICKS_TO_MS


    return top_contributors_ranked, bound_type, eval_time, render_time
    

