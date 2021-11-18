#!/bin/bash
# Two facultativ parameters : -f <nameOfTheVideoFile> and -i <URL_Output>
name="rtsp://rtsp-server:8554/people_london"
sdp="rtsp://:8559/flux";
sout="#transcode{vb=0,scale=0,acodec=mpga,ab=128,channels=2,samplerate=44100}:rtp{sdp="$sdp"}";
su vlcuser -c "cvlc -vvv $name --sout '$sout'"
