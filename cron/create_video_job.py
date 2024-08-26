import cloudinary.uploader
import cv2
import os
import datetime
import cloudinary

IMAGE_FOLDER = "./images"
VIDEO_FOLDER = "./videos"

def create_video():
    time_stamp = datetime.datetime.now().isoformat()
    print(time_stamp)
    video_writer = None
    for file in sorted(os.listdir(IMAGE_FOLDER),
                      key=lambda item : os.path.getctime(
                          os.path.join(IMAGE_FOLDER, item)
                      )):
        file_path = os.path.join(IMAGE_FOLDER, file)
        frame = cv2.imread(file_path)
        os.remove(file_path) # remove file after reading
        if not video_writer:
            hieght, width, _ = frame.shape
            video_path = f"{VIDEO_FOLDER}/video_{time_stamp}.avi"
            video_writer = cv2.VideoWriter(video_path, 0, 10,
                                           (width, hieght))
        
        video_writer.write(frame)
    
    cv2.destroyAllWindows()
    if video_writer: video_writer.release()
    
    for file in sorted(os.listdir(VIDEO_FOLDER),
                key=lambda item : os.path.getctime(
                    os.path.join(VIDEO_FOLDER, item)
                )):
        try:
            file_path = os.path.join(VIDEO_FOLDER, file)
            print(file_path)
            cloudinary.uploader.upload_large(
                file_path,
                resource_type="video",
                chunk_size=6_000_000
            )
            os.remove(file_path)
        except:
            print("Could not be send", file_path)