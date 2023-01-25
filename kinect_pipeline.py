from freenect2 import Device, FrameType
import numpy as np
import cv2

path_save = "/home/ebouhanna/Documents/Pro/Mines/3A/Mareva/mini_projet/"

def callback(type_, frame):
    if type_ == FrameType.Color:
        rgb = frame.to_array().astype(np.uint8)[:, :, 0:3] # BGRX format, need to get rid of the last one
        cv2.imshow('rgb', rgb)
    elif type_ == FrameType.Depth:
        rgb = None
    else:
        rgb = None
    return rgb

# Initialize video to be save
video_save = []

# Start kinect
device = Device()
device.start()
color_params = device.color_camera_params
print(f"Color params : fx={color_params.fx}, fy={color_params.fy}, cx={color_params.cx}, cy={color_params.cy}")

while True:
    type_, frame = device.get_next_frame()
    res = callback(type_, frame)
    if res is not None:
        video_save.append(res)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        device.stop()
        break

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(path_save + 'test_kinect.mp4', fourcc, 5.0, (video_save[0].shape[1], video_save[0].shape[0]))
print(video_save[0].shape)
for i in range(len(video_save)):
    out.write(video_save[i])
out.release()
print('Released video')
        
    
