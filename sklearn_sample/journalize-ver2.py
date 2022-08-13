import glob
import shutil
import time

if __name__ == "__main__":
    for image_path in glob.glob('data/num_dataset/train/*.jpg'):
        digit = image_path[28:]
        if digit == "ones.jpg":
            shutil.move(image_path, "data/num_dataset/train/ones")
        elif digit == "tens.jpg":
            shutil.move(image_path, "data/num_dataset/train/tens")
        else:
            shutil.move(image_path, "data/num_dataset/train/minutes")
        time.sleep(0.01)
