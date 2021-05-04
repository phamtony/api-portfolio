def allowed_image(filename, app):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def image_ext(filename):
    return str(filename.rsplit(".", 1)[1])