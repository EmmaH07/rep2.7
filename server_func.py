import glob
import os
import shutil
import subprocess
import base64
from PIL import Image, ImageGrab
import logging
from io import BytesIO

ERR = b"An error accrued"
SUC = b"Executed successfully"


def dir_cmd(path):
    files_path = path + r'\*.*'
    try:
        d_list = glob.glob(files_path)
        d_string = " "
        return bytes(d_string.join(d_list), 'utf-8')
    except FileNotFoundError:
        return ERR
    except RuntimeError:
        return ERR


def delete(file_path):
    try:
        os.remove(file_path)
        return SUC
    except FileNotFoundError:
        return ERR
    except RuntimeError:
        return ERR


def copy(file1, file2):
    try:
        shutil.copy(file1, file2)
        return SUC

    except shutil.SameFileError:
        return ERR

    except PermissionError:
        return ERR

    except ValueError:
        return ERR

    except OSError:
        return ERR

    except RuntimeError:
        return ERR

    except Exception:
        return ERR


def exe(path):
    try:
        subprocess.call(path)
        return SUC
    except OSError:
        return ERR
    except RuntimeError:
        return ERR

    except Exception:
        return ERR


def take_screenshot():
    try:
        im = ImageGrab.grab()
        im.save("server_screenshot.jpg")
        return SUC
    except RuntimeError:
        return ERR

    except Exception:
        return ERR


def send_screenshot():
    try:
        with open('server_screenshot.jpg', 'rb') as img:
            return_value = base64.b64encode(img.read()).decode('utf-8')

        # Remove the redundant image
        os.remove('server_screenshot.jpg')
    except OSError as err:
        logging.error(f"os error while trying to take a screenshot: {err}")
        # Return error code
        return_value = ''

    return return_value.encode()


def is_valid_req(request):
    req_list = ["DIR", "DELETE", "COPY", "EXECUTE", "TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT"]
    for item in req_list:
        if request == item:
            return True
    return False


def decode_image(base64_bytes):
    """
    Decode a base64-encoded image, save it to a file, and show it.

    :param base64_bytes: The base64-encoded image data.
    :type base64_bytes: bytes

    :return: None
    """
    try:
        base64str = base64_bytes.decode()
        # Decode the base64 string back to image data
        decoded_image = base64.b64decode(base64str)

        # Create a PIL Image object from the decoded image data
        image = Image.open(BytesIO(decoded_image))
        image.save('output_image.jpg')
        image.show()

    except Exception as err:
        print(str(err))
