import shutil
import argparse
import numpy as np
from PIL import Image
from pathlib import Path


def parse_arg():

    parser = argparse.ArgumentParser(prog="Merge Global session tiles")

    parser.add_argument("-pi", "--path-in-folder", required=True, default="", help="Path to folder where the global tiles folder are. Use symlink to gather them.")
    parser.add_argument("-po", "--path-out-folder", required=True, default="", help="Path to output the global tiles")

    return parser.parse_args()


def merge_two_images(x1: Path, x2: Path):
    """ Merge x2 into x1 """

    if not x1.exists() or not x1.is_file():
        print(f"First image not found {x1}")
        return
    
    if not x2.exists() or not x2.is_file():
        print(f"Second image not found {x2}")
        return
    
    if x2.stat().st_size == 334: return # No need to write image, nothing inside
    if x1.stat().st_size == 334: 
        # Save the second image inside the first one
        shutil.copy(x2, Path(x1.parent, x2.name))
        return
    
    im1 = Image.open(x1)
    im2 = Image.open(x2)

    img1_array = np.array(im1)
    img2_array = np.array(im2)

    
    # Initialize an empty array for the result
    mean_image_array = np.zeros_like(img1_array, dtype=np.float32)

    # Loop through the RGB channels (0: Red, 1: Green, 2: Blue)
    for i in range(3):
        # If both pixels have non-zero alpha, average the RGB values
        mean_image_array[..., i] = np.where(img1_array[..., 3] != 0, img1_array[..., i], img2_array[..., i])
                                            
    # For the alpha channel (3rd index), we just take it from the image where the alpha is not zero
    mean_image_array[..., 3] = np.where(img1_array[..., 3] != 0, img1_array[..., 3], img2_array[..., 3])

    # Convert back to uint8
    mean_image_array = mean_image_array.astype(np.uint8)

    # Convert the array back to an image
    mean_image = Image.fromarray(mean_image_array, 'RGBA')

    mean_image.save(x1)

def main(opt: argparse.Namespace):

    # Base path.
    ROOT_FOLDER = Path(opt.path_out_folder)
    if not ROOT_FOLDER.exists() or not ROOT_FOLDER.is_dir():
        raise NameError("Root folder not found at: ", ROOT_FOLDER)
    global_tiles_folder = Path(ROOT_FOLDER, "global_tile")

    # Clean global dir.
    shutil.rmtree(global_tiles_folder, ignore_errors=True)
    global_tiles_folder.mkdir(exist_ok=True, parents=True)

    # Iter on each tiles_folder
    INPUT_FOLDER = Path(opt.path_in_folder)
    if not INPUT_FOLDER.exists() or not INPUT_FOLDER.is_dir():
        raise NameError("Root folder not found at: ", INPUT_FOLDER)

    list_tiles_folder = sorted(list(INPUT_FOLDER.iterdir()))
    for j, folder in enumerate(list_tiles_folder):
        print(f"{j+1}/{len(list_tiles_folder)}: Work with {folder}")

        for zoom_level in sorted(list(folder.iterdir())):
            if not zoom_level.is_dir(): continue
            print(f"* Zoom level: {zoom_level.name}")
            for y in zoom_level.iterdir():
                y_g = Path(global_tiles_folder, zoom_level.name, y.name)
                y_g.mkdir(exist_ok=True, parents=True)
                y_files = [a.name for a in y_g.iterdir()]

                for x in y.iterdir():
                    if x.name not in y_files:
                        shutil.copy(x, Path(y_g, x.name))
                    else:
                        merge_two_images(Path(y_g, x.name), x)

if __name__ == "__main__":
    opt = parse_arg()
    main(opt)