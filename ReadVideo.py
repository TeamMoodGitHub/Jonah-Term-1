import numpy
import cv2

INPUT_VOD_PATH = "F:\\Work\\CvTest\\smashvid.mp4"
VOD_NAME = "SmashVid"

def get_frames():
    video = cv2.VideoCapture(INPUT_VOD_PATH)
    # forward over to the frames you want to start reading from.
    video.set(1,12200);
    success, frame = video.read()
    count = 0
    file_count = 0
    success = True
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Loading video %d seconds long with FPS %d and total frame count %d " % (total_frame_count/fps, fps, total_frame_count))

    while success:

        success, frame = video.read()
        if count % 100 == 0:
            print("Currently at frame ", count)

        # i save once every 15 frames, which comes out to 2 frames per second.
        # i think anymore than 2 FPS leads to to much repeat data.
        if count % 120 == 0:
            cv2.imwrite("F:\\Work\\CvTest\\frames\\frame_%d.jpg" %  (file_count), frame)
            file_count += 1
        count += 1

    print("Saved %d frames" % (file_count) )


if __name__ == "__main__":
    get_frames()