import cv2
import numpy as np

width = 1280
height = 720
filepath = "../colorImg.dat"


if __name__ == "__main__":
    np_mmap = np.memmap(
        filepath,
        dtype='uint8',
        mode='r',
        shape=(height, width, 4),
    )

    while True:
        key = cv2.waitKey(50)
        if key == 27:  # ESC
            break
        cv2.imshow('mmap image', np_mmap)

    cv2.destroyAllWindows()