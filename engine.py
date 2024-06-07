import os

import pytesseract
from PIL import Image


def photo_to_text(path_to_photo: str) -> str:
    try:
        text = pytesseract.image_to_string(Image.open(path_to_photo),
                                           lang='rus+eng', timeout=10)
    except RuntimeError as e:
        text = e
    except Exception:
        text = False
    finally:
        os.remove(path_to_photo)
    return text


pytesseract.pytesseract.tesseract_cmd = r'/opt/local/bin/tesseract'
