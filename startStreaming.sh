export DEST_IP=192.168.1.142
gst-launch-1.0 v4l2src ! video/x-raw,width=640,height=480,framerate=30/1 ! vpuenc_h264 bitrate=500 ! rtph264pay ! udpsink host=$DEST_IP port=5000 sync=false -v
