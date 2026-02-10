import glob
import os


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        try:
            os.remove(image)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    clean_folder()