import os, gi, json, gpustat
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from datetime import datetime, timezone

DEBUG_FOLDER = os.environ.get('DEBUG_FOLDER')
GRAPHS_FOLDER = os.environ.get('GST_DEBUG_DUMP_DOT_DIR')
GPU_STATS_FOLDER = f"{os.environ.get('DEBUG_FOLDER')}/gpu_stats"

def save_graph(pipeline, event, graph_name, save_gpu_stats=False):
    time = datetime.now(timezone.utc).astimezone().isoformat()
    os.makedirs(GRAPHS_FOLDER, exist_ok=True)
    dotfile = os.path.abspath(f"{GRAPHS_FOLDER}/{graph_name}_{event}_{time}.dot")
    pngfile = os.path.abspath(f"{GRAPHS_FOLDER}/{graph_name}_{event}_{time}.png")
    if os.access(dotfile, os.F_OK):
        os.remove(dotfile)
    if os.access(pngfile, os.F_OK):
        os.remove(pngfile)
    if save_gpu_stats:
        save_gpu_stats_to_json(graph_name, event, time)

    Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, f"{graph_name}_{event}_{time}")
    os.system('/usr/bin/dot' + " -Tpng -o " + pngfile + " " + dotfile)

def save_gpu_stats_to_json(name, event, time):
    os.makedirs(GPU_STATS_FOLDER, exist_ok=True)
    gpustatsfile = os.path.abspath(f"{GPU_STATS_FOLDER}/{name}_{event}_{time}.json")
    if os.access(gpustatsfile, os.F_OK):
        os.remove(gpustatsfile)
    try:
        stats_json = gpustat.new_query().jsonify()
        if "gpus" in stats_json:
            with open(gpustatsfile, 'w') as outfile:
                json.dump(stats_json, outfile, default=str)
        else:
            raise Exception("ImcompleteJsonFile")
    except Exception as e:
        print(f"It was not possible to save gpu stats json. Error: {e}")
