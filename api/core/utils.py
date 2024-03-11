from PIL import Image


def is_valid_image(image):
    try:
        image = Image.open(image)
        image.verify()
        return True
    except:
        return False
