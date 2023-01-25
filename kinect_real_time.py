from IPython import display
from openvino.runtime import Core
import collections
import cv2
import os
from utils import *
import time
from freenect2 import Device, FrameType

def run_object_detection(source=0, flip=False, use_popup=False, skip_first_frames=0):
    device = None
    video_frames = []
    masks = None
    dist = []
    
    try:
        device = Device()
        device.start()        
        
        if use_popup:
            title = "Press ESC to Exit"
            cv2.namedWindow(
                winname=title, flags=cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE
            )

        processing_times = collections.deque()
        visualizer = InstanceSegmentationVisualizer(classes, True, True)
        
        # init count depth
        t0 = time.time()
        while True:            
            # Grab the frame.
            type_, frame_ = device.get_next_frame()
            if frame_ is None:
                print("Source ended")
                break
                
            if type_ == FrameType.Color:
                frame = frame_.to_array().astype(np.uint8, copy=True)[:,:,0:3]

                # If the frame is larger than full HD, reduce size to improve the performance.
                scale = 1280 / max(frame.shape)
                if scale < 1:
                    frame = cv2.resize(
                        src=frame,
                        dsize=None,
                        fx=scale,
                        fy=scale,
                        interpolation=cv2.INTER_AREA,
                    )
                    
                cv2.resize(src=frame, dsize=(640, 480), interpolation=cv2.INTER_AREA, dst=frame)

                # Resize the image and change dims to fit neural network input.
                input_img = cv2.resize(
                    src=frame, dsize=(width, height), interpolation=cv2.INTER_AREA
                )
                # Create a batch of images (size = 1).
                input_img = input_img[np.newaxis, ...]
                input_img = np.moveaxis(input_img, -1, 1)

                # Measure processing time.

                start_time = time.time()
                # Get the results.
                results = list(compiled_model([input_img]).values())
                stop_time = time.time()
                # Get network outputs
                labels, scores, boxes, masks = process_results(frame=frame, input_img=input_img, results=results)
                # visualize
                frame = visualizer(frame, boxes, labels, scores, masks, dist, None, None)

                processing_times.append(stop_time - start_time)
                # Use processing times from last 200 frames.
                if len(processing_times) > 200:
                    processing_times.popleft()

                _, f_width = frame.shape[:2]
                # Mean processing time [ms].
                processing_time = np.mean(processing_times) * 1000
                fps = 1000 / processing_time
                cv2.putText(
                    img=frame,
                    text=f"Inference time: {processing_time:.1f}ms ({fps:.1f} FPS)",
                    org=(20, 40),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    fontScale=f_width / 1000,
                    color=(0, 0, 255),
                    thickness=1,
                    lineType=cv2.LINE_AA,
                )
                
                video_frames.append(frame)

                # Use this workaround if there is flickering.
                if use_popup:
                    cv2.imshow(winname=title, mat=frame)
                    key = cv2.waitKey(1)
                    # escape = 27
                    if key == 27:
                        break
                else:
                    # Encode numpy array to jpg.
                    _, encoded_img = cv2.imencode(
                        ext=".jpg", img=frame, params=[cv2.IMWRITE_JPEG_QUALITY, 100]
                    )
                    # Create an IPython image.
                    i = display.Image(data=encoded_img)
                    # Display the image in this notebook.
                    display.clear_output(wait=True)
                    display.display(i)
                
                del frame
                    
            elif type_ == FrameType.Depth:
                t1 = time.time()
                if t1 - t0 > 1:
                    frame_depth = frame_.to_array().astype(float)
                    cv2.resize(src=frame_depth, dsize=(640, 480), interpolation=cv2.INTER_AREA, dst=frame_depth)
                    # list of distances for each mask
                    dist = get_distance_to_humans(frame_depth, masks)
                    del frame_depth
                    t0 = time.time()

                

    # ctrl-c
    except KeyboardInterrupt:
        print("Interrupted")
    
    # any different error
    except RuntimeError as e:
        print(e)
    finally:
        if device is not None:
            # Stop capturing.
            device.stop()
            device.close()
        if use_popup:
            cv2.destroyAllWindows()
        return video_frames

# Define path to models
base_model_dir = "models/model-segmentation"
model_segmentation = "instance-segmentation-person-0007"
converted_model_path = f"models/model-segmentation/intel/{model_segmentation}/FP16/{model_segmentation}.xml"

# Initialize OpenVINO Runtime.
ie_core = Core()
# Read the network and corresponding weights from a file.
model = ie_core.read_model(model=converted_model_path)
# Compile the model for CPU (you can choose manually CPU, GPU, MYRIAD etc.)
# or let the engine choose the best available device (AUTO).
compiled_model = ie_core.compile_model(model=model, device_name="CPU")

# Get the input and output nodes.
input_layer = compiled_model.input(0)
output_boxes = compiled_model.output(0)

# Get the input size.
height, width = list(input_layer.shape)[2:4]

classes = [
    "person", "background", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "street sign", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant",
    "bear", "zebra", "giraffe", "hat", "backpack", "umbrella", "shoe", "eye glasses",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "plate", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "mirror", "dining table", "window", "desk", "toilet",
    "door", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "blender", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush", "hair brush"
]
video_frames = run_object_detection(source=0, flip=True, use_popup=True)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('test_kinect_script.mp4', fourcc, 5, (video_frames[0].shape[1], video_frames[0].shape[0]))
for i in range(len(video_frames)):
    out.write(video_frames[i])
out.release()