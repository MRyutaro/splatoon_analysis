import cv2
import glob
import shutil


def show_images(selected_images):
    for i in range(len(selected_images)):
        show_image(cv2.imread(
            selected_images[i]), f"{i}", (200, 320), (1650-200*i, 350))


def show_image(image, window_name, image_size, image_pos):
    cv2.imshow(window_name, cv2.resize(image, image_size))
    cv2.moveWindow(window_name, image_pos[0], image_pos[1])


def journal_image(input_key, image_path):
    if input_key == 27:
        exit()
    key_code = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
    for i, key_num in enumerate(key_code):
        if input_key == key_num:
            # print(f"{image_path}は{i}です")
            move_dir(i, image_path)
            return


def move_dir(after_dir, before_dir):
    after_dir = f"{before_dir[:23]}{after_dir}"
    print(before_dir[23:], "の移動後のフォルダ->", after_dir)
    shutil.move(before_dir, after_dir)


if __name__ == "__main__":
    while True:
        images = glob.glob('data/num_dataset/train/ones/*.jpg')
        show_images(images[0:8])
        journal_image(, images[0])
