#!/usr/bin/env python
import sys, json

import gi, pyds, configparser
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib
from ds_utils.is_aarch_64 import is_aarch64

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def cb_newpad(decodebin, decoder_src_pad, sinkpad):
    caps=decoder_src_pad.get_current_caps()
    gststruct=caps.get_structure(0)
    gstname=gststruct.get_name()

    features=caps.get_features(0)

    if(gstname.find("video")!=-1):
        decoder_src_pad.link(sinkpad)

def main(args):
    if len(args) != 2:
        sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
        sys.exit(1)

    GObject.threads_init()
    Gst.init(None)

    pipeline = Gst.Pipeline()
    uridecodebin = Gst.ElementFactory.make("uridecodebin", "sourcebin")
    if not uridecodebin:
        sys.stderr.write("'uridecodebin' gstreamer plugin missing\n")
        sys.exit(1)

    streammux = Gst.ElementFactory.make("nvstreammux", "mux")
    streammux.set_property("width", 640)
    streammux.set_property("height", 480)
    streammux.set_property("batched-push-timeout", 40000)
    streammux.set_property("batch-size", 1)  
    streammux.set_property("live-source", 1)

    detector = Gst.ElementFactory.make("nvinfer", "primary-inference"); assert detector
    tracker = Gst.ElementFactory.make("nvtracker", "tracker"); assert tracker
    nvdsanalytics = Gst.ElementFactory.make("nvdsanalytics", "nvdsanalytics"); assert nvdsanalytics

    # Setting elements properties
    detector.set_property('config-file-path', "/app/config/nvinfer_detector_config.txt")

    pgie_batch_size=detector.get_property("batch-size")

    if(pgie_batch_size != 1):
        print(f"Overriding infer-config batch-size {pgie_batch_size} with max batch size 1")
    detector.set_property("batch-size",1)

    tracker_config = configparser.ConfigParser()
    tracker_config.read("/app/config/nvtracker_tracker_config.txt")
    tracker_config.sections()

    for key in tracker_config['tracker']:
        if key == 'tracker-width' :
            tracker_width = tracker_config.getint('tracker', key)
            tracker.set_property('tracker-width', tracker_width)
        if key == 'tracker-height' :
            tracker_height = tracker_config.getint('tracker', key)
            tracker.set_property('tracker-height', tracker_height)
        if key == 'gpu-id' :
            tracker_gpu_id = tracker_config.getint('tracker', key)
            tracker.set_property('gpu_id', tracker_gpu_id)
        if key == 'll-lib-file' :
            tracker_ll_lib_file = tracker_config.get('tracker', key)
            tracker.set_property('ll-lib-file', tracker_ll_lib_file)
        if key == 'll-config-file' :
            tracker_ll_config_file = tracker_config.get('tracker', key)
            tracker.set_property('ll-config-file', tracker_ll_config_file)
        if key == 'enable-batch-process' :
            tracker_enable_batch_process = tracker_config.getint('tracker', key)
            tracker.set_property('enable_batch_process', tracker_enable_batch_process)

    nvdsanalytics.set_property('config-file', "/app/config/config_nvdsanalytics.txt") 
    nvdsanalytics.set_property('enable', 0)

    tiler = Gst.ElementFactory.make("nvmultistreamtiler", "tiler"); assert tiler
    tiler.set_property("width", 640)
    tiler.set_property("height", 480)
    tiler.set_property("columns",1)
    tiler.set_property("rows",1)

    osd_convertor = Gst.ElementFactory.make("nvvideoconvert", "osd_convertor"); assert osd_convertor
    nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay"); assert nvosd
    nvosd.set_property('process-mode', 1)
    nvosd.set_property('display-text', 1)
    if is_aarch64():
        transform = Gst.ElementFactory.make("nvegltransform", "nvegl-transform"); assert transform
    videosink = Gst.ElementFactory.make("autovideosink", "videosink"); assert videosink
    videosink.set_property("sync", 0)

    pipeline.add(uridecodebin)
    pipeline.add(streammux)
    pipeline.add(detector)
    pipeline.add(tracker)
    pipeline.add(nvdsanalytics)
    pipeline.add(tiler)
    pipeline.add(videosink)
    pipeline.add(osd_convertor)
    if is_aarch64():
        pipeline.add(transform)
    pipeline.add(nvosd)
    streammux.link(detector)
    detector.link(tracker)
    tracker.link(nvdsanalytics)
    nvdsanalytics.link(tiler)
    tiler.link(osd_convertor) 
    osd_convertor.link(nvosd)
    if is_aarch64():
        nvosd.link(videosink)
        transform.link(videosink)
    else:
        nvosd.link(videosink)

    # take the commandline argument and ensure that it is a uri
    if Gst.uri_is_valid(args[1]):
      uri = args[1]
    else:
      uri = Gst.filename_to_uri(args[1])
    uridecodebin.set_property('uri', uri)

    uridecodebin.connect("pad-added", cb_newpad, streammux.get_request_pad("sink_0"))

    # create and event loop and feed gstreamer bus mesages to it
    loop = GObject.MainLoop()

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)
    
    # start play back and listed to events
    pipeline.set_state(Gst.State.PLAYING)
    try:
      loop.run()
    except:
      pass
    
    # cleanup
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))