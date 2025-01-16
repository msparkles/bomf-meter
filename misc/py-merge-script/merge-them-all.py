from functools import reduce
from pathlib import Path
import math
import sys

from PIL import Image
import numpy as np

def merge_images(file_paths):
    images = list(map(Image.open, file_paths))

    size_sum: tuple[int, int] = reduce(
        lambda a, b:
            tuple(n + m for n, m in zip(a, b)),
        map(lambda x: x.size, images)
    )
    target_size: tuple[int, int] = tuple(map(lambda n: 2 ** math.ceil(math.log2(n / len(images))), size_sum))
    print('Target size:', target_size)

    images = list(map(lambda image: image.resize(target_size, Image.Resampling.LANCZOS).convert('RGB'), images))
    image_arrays = list(map(np.asarray, images))

    px = np.array([[(0, 0, 0)],])
    px = np.resize(px, [*target_size, 3])

    for a in image_arrays:
        px += a
    px = px / len(images)

    Image.fromarray(np.uint8(px)).show()

    for image in images:
        image.close()

def main() -> int:
    file_paths = []

    for line in sys.stdin:
        input_paths = list(map(Path, map(str.strip, line.strip().split(' '))))
        file_paths.extend(input_paths)

    print('Files count:', len(file_paths))

    merge_images(file_paths)

    return 0

if __name__ == '__main__':
    sys.exit(main())