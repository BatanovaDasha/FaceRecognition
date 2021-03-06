import cv2
import numpy as np
import scipy.misc
import scipy.ndimage
import skimage.transform

from utils.logger import Logger

base_actions_logger = Logger('BaseActions')


def open_image(filename: str, greyscale: bool = False) -> np.array:
    """
    Function that opens image file and returns it's representation as numpy array
    In case where file doesn't exist - logs error.
    :param filename: image file name to open.
    :param greyscale: if True image will be read as greyscale, else - rgb.
    :return: numpy array representation of image
    """
    try:
        return cv2.imread(filename, not greyscale)
    except FileNotFoundError as e:
        base_actions_logger.log_string(f'Failed to open image: {filename} due to {e}')
        return None


def save_image(image: np.array, path_to_file: str) -> bool:
    """
    Used to save image to file. Returns True if operation succeeded false otherwise.
    :param image: numpy repr. of an image. (Numpy array)
    :param path_to_file: filename where to save result.
    :return: True if operation succeed False otherwise.
    """
    try:
        scipy.misc.imsave(path_to_file, image)
        return True
    except BaseException as e:
        base_actions_logger.log_string(f'Failed to save {path_to_file} due to {e}.')
        return False


def resize_image(image: np.array, target_size: tuple) -> np.array:
    """
    Wrapper for resize function from skimage. Returns result of resizing image to target size,
    in case of error logs information about it.
    :param image: source image to be resized
    :param target_size: tuple of two integer values, x and y dimensions of result image.
    :return: result of resizing, None if error happens.
    """
    try:
        return skimage.transform.resize(image, target_size)
    except BaseException as e:
        base_actions_logger.log_string(f'Failed to rescale image to size {target_size} due to {e}')
        return None


def crop_image_part(source_image: np.array, crop_from_to: tuple) -> np.array:
    """
    Function that crops image from start point to end point
    :param source_image: numpy array representation of source image
    :param crop_from_to: tuple with 4 values, start x and y and end x and y
    (10, 10, 20, 20) means crop from point (10,10) to (20,20)
    :return: numpy array representation of image fragment, None in case of errors.
    """
    from copy import deepcopy
    try:
        # noinspection PyTupleAssignmentBalance
        # assuming we have enough values in statement.
        x_start, y_start, x_end, y_end = (*crop_from_to,)
        crop_target = deepcopy(source_image)[x_start:x_end, y_start:y_end]
        return crop_target
    except BaseException as e:
        base_actions_logger.log_string(f'Failed to crop image with {crop_from_to} parameters due to {e}.')
        return None


def draw_rectangle(image: np.array, coordinates: tuple, color: tuple = (0, 0, 0)) -> np.array:
    """
    Returns image with rectangle drawn on it, rectangle thickness is set to 2 px.
    :param image: source image of type np.array
    :param coordinates: x start, y start, x end, y end tuple.
    :param color: tuple representing desired color.
    :return: image with drawn rectangle on it.
    """
    x_start, y_start, x_end, y_end = coordinates
    return cv2.rectangle(image, (x_start, y_start), (x_end, y_end), color, 6)


###TODO: Implement it.
def normalize_image():
    pass


def equalize_histogram(img: np.array) -> np.array:
    """
    Returns image with equalized histogram. Wrapper for cv2.equalizeHist
    :param img: numpy array representation of source image (greyscale).
    :return: numpy array repr. of image with equalized histogram.
    """
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(img)
