import os
import shutil
import rawpy
import rawpy.enhance
import exifread
import filetype

import matplotlib.pyplot as plt

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True  # Support for loading partially corrupt files

def get_file_list(directory_path):
    """
        Creates directories for invalid and corrupt files and returns a list of all files in the folder.

        Args:
            directory_path (str): Directory housing images being considered

        Returns:
            files (list): List of files present in the target directory
        """
    # Make Invalid and Corrupt directories if they don't exist
    if not os.path.exists(directory_path + "\\" + "Invalid"):
        os.makedirs(directory_path + "\\" + "Invalid")

    if not os.path.exists(directory_path + "\\" + "Corrupt"):
        os.makedirs(directory_path + "\\" + "Corrupt")

    # Return a list of all files in the directory
    files = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            files.append(entry)
    return files

def get_exif_data(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        for key, value in tags.items():
            if key != 'JPEGThumbnail':  # do not print (uninteresting) binary thumbnail data
                print(f'{key}: {value}')

def count_pixel_colors(files, directory_path):
    """
    Counts the occurrences of each unique pixel color in a JPG image.

    Args:
        directory_path (str): Directory housing images being considered
        files (list): List of files present in the target directory

    Returns:
        dict: A dictionary where keys are RGB tuples (pixel colors) and
              values are the counts of those colors.
    """
    # TODO make sure things don't end up in both corrupt and invalid
    for file in files:
        image_path = os.path.join(directory_path, file)
        #print("Processing " + image_path.rsplit("\\", 1)[1])

        # Identify format
        img_format = file.rsplit(".", 1)[1]

        # Scrape off any files too corrupt to know what kind of file they are
        kind = filetype.guess(image_path)
        if kind is None:
            print(image_path.rsplit("\\", 1)[1] + " has an extension of " + img_format + " but its type cannot be guessed.\n")
            shutil.move(image_path, os.path.join(directory_path, "Corrupt"))
            continue

        # Handle CR2
        if img_format == "CR2":

            # If file cannot be opened or is not identifiable as RAW, move to corrupt directory
            try:
                rawpy.imread(image_path)

            except Exception:
                print(image_path.rsplit("\\", 1)[1] + " cannot be opened.\n")
                shutil.move(image_path, os.path.join(directory_path, "Corrupt"))
                continue

            # Attempt to process image and warn of corrupt data if found
            with rawpy.imread(image_path) as raw:
                try:
                    img = raw.postprocess()
                    rgb_img = Image.fromarray(img)
                    #plt.imshow(rgb_img)

                except IOError:
                    print("Input/Output error. Check " + image_path.rsplit("\\", 1)[1] + " manually.\n")
                    shutil.move(image_path, os.path.join(directory_path, "Invalid"))
                    continue

                except Exception as e:
                    raw.close()
                    print("Check " + image_path.rsplit("\\", 1)[1] + " manually.\n")
                    shutil.move(image_path, os.path.join(directory_path, "Invalid"))
                    continue

        # Handle JPG
        else:
            try:
                with Image.open(image_path) as img:
                    rgb_img = img.convert('RGB')

            except Exception:
                print("\n")
                continue

        # Iterate through each pixel and count its color
        pixel_counts = {}

        width, height = rgb_img.size
        total_pixels = width * height

        for x in range(width):
            for y in range(height):

                try:
                    pixel_color = rgb_img.getpixel((x, y))

                    pixel_counts[pixel_color] = pixel_counts.get(pixel_color, 0) + 1
                    #print(pixel_color)

                except Exception as e:
                    print(e)
                    print(image_path.rsplit("\\", 1)[1] + " requires manual check.\n")
                    continue

        is_valid = True
        for color, count in pixel_counts.items():
            percent = count / total_pixels * 100

            # If more than 50% of the pixels are the same color, declare invalid and move
            if percent > 50:
                print(image_path.rsplit("\\", 1)[1] + f" is {percent} one color.\n")
                is_valid = False
                break

        if not is_valid:
            shutil.move(image_path, os.path.join(directory_path, "Invalid"))


count_pixel_colors(get_file_list(r'\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\WorkingDirectory\2014_04818\Drive 3\New Photos\10-19-08 McCain\7 toledo, oh Rally'),
                   r'\\libfile.lib.asu.edu\share\Archivematica\ms_cm_mss_409\WorkingDirectory\2014_04818\Drive 3\New Photos\10-19-08 McCain\7 toledo, oh Rally')
