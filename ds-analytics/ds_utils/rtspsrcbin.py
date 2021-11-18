import time
import numpy as np
from threading import Lock
from enum import Enum

class BinState(Enum):
    INITIALIZING = 1
    STARTING = 2
    PAUSED = 3
    PLAYING = 4
    RESETING = 5
    NULL = 6
    FAILURE = 7
    RETRYING = 8
    READY = 9
    REMOVED = 10


class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    IMPORTANT = 2
    CRITICAL = 3


class Event():
    def __init__(self, event_type: str, time, priority: EventPriority = EventPriority.NORMAL):
        self._priority = priority
        self._time = time
        self._type = event_type

    @property
    def priority(self):
        return self._priority

    @property
    def time(self):
        return self._time

    @property
    def type(self):
        return self._type


class NvDsSrcBin():
    def __init__(self, uri, name, rtsp_reconnect_interval_sec, streammux):
        self._bin = None
        self._uri = uri
        self._name = name
        self._rtsp_reconnect_interval_sec = rtsp_reconnect_interval_sec
        self._streammux = streammux
        self._bin_lock = Lock()
        self._last_reconnect_time = time.time()
        self._last_buffer_time = time.time()
        self._state = BinState.INITIALIZING
        self._pipeline = None
        self._async_state_watch_running = False
        self._source_started = False
        self._status_callback_id = None
        self._internal_id = None
        self._external_id = None
        self._reconfiguring = False
        self._tee = False
        self._last_event = None
        self._in_fallback = False
        self._osd_data = {}

    @property
    def bin(self):
        return self._bin

    @property
    def uri(self):
        return self._uri

    @property
    def name(self):
        return self._name

    @property
    def rtsp_reconnect_interval_sec(self):
        return self._rtsp_reconnect_interval_sec

    @property
    def streammux(self):
        return self._streammux

    @property
    def last_reconnect_time(self):
        return self._last_reconnect_time

    @property
    def last_buffer_time(self):
        return self._last_buffer_time

    @property
    def state(self):
        return self._state

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def async_state_watch_running(self):
        return self._async_state_watch_running

    @property
    def internal_id(self):
        return self._internal_id

    @property
    def external_id(self):
        return self._external_id

    @property
    def source_started(self):
        return self._source_started

    @property
    def reconfiguring(self):
        return self._reconfiguring

    @property
    def status_callback_id(self):
        return self._status_callback_id

    @property
    def tee(self):
        return self._tee

    @property
    def last_event(self):
        return self._last_event

    @property
    def in_fallback(self):
        return self._in_fallback

    @property
    def osd_data(self):
        return self._osd_data

    @bin.setter
    def bin(self, value):
        self._bin = value

    @bin.setter
    def bin(self, value):
        self._bin = value

    @name.setter
    def name(self, value):
        self._name = value

    @uri.setter
    def uri(self, value):
        self._uri = value

    @state.setter
    def state(self, value):
        self._state = value

    @pipeline.setter
    def pipeline(self, value):
        self._pipeline = value

    @last_buffer_time.setter
    def last_buffer_time(self, time):
        with self._bin_lock:
            self._last_buffer_time = time

    @last_reconnect_time.setter
    def last_reconnect_time(self, time):
        self._last_reconnect_time = time

    @async_state_watch_running.setter
    def async_state_watch_running(self, value):
        self._async_state_watch_running = value

    @internal_id.setter
    def internal_id(self, value):
        self._internal_id = value

    @external_id.setter
    def external_id(self, value):
        self._external_id = value

    @source_started.setter
    def source_started(self, value):
        self._source_started = value

    @reconfiguring.setter
    def reconfiguring(self, value):
        self._reconfiguring = value

    @status_callback_id.setter
    def status_callback_id(self, value):
        self._status_callback_id = value

    @tee.setter
    def tee(self, value):
        self._tee = value

    @last_event.setter
    def last_event(self, value: Event):
        self._last_event = value

    @in_fallback.setter
    def in_fallback(self, value):
        self._in_fallback = value

    @osd_data.setter
    def osd_data(self, value):
        self._osd_data = value