# import the necessary packages
from picamera import PiCamera
from picamera.array import PiRGBArray
import threading
import cv2
import boto3
import time
import os

from datetime import datetime

USERID = "8787878787"
# get credentials in env
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECERT_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')

bucket_resource = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECERT_ACCESS_KEY,
    region_name="us-east-1"
)
bucket = bucket_resource.Bucket('team16')

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
		# initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False
        
    def start(self):
        # start the thread to read frames from the video stream
        threading.Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)
            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            
    def read(self):
        # return the frame most recently read
        return self.frame
    
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

def push_image(image):
    st = time.time()
    # # grab an image from the camera
    image_name = '{}.jpg'.format(int(datetime.utcnow().timestamp()))
    local_path = './shotted_image/{}'.format(image_name)
    cv2.imwrite(local_path, image)

    # initialize S3 bucket
    s3_key = 'final-project/{}/{}'.format(USERID, image_name)
    bucket.upload_file(local_path, s3_key)
    print("Upload time: {}".format(time.time() - st))

if __name__ == "__main__":
    vs = PiVideoStream((480, 360)).start()
    # vs = PiVideoStream().start()
    time.sleep(2)
    
    start_time = time.time()
    while 1:
        frame = vs.read()
        cv2.imshow("Frame", frame)
        
        if time.time() - start_time > 5:
            push_image(frame)
            start_time = time.time()
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Stop")
            break
    
    vs.stop()