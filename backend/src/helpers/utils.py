import base64
from io import BytesIO

from PIL import Image


def webp_2_others(base64_webp_str: str, fmt: str = "JPEG") -> bytes:
    """convert webp base64 string to `fmt` type image
    Args:
        base64_webp_str(str): webp image base64 string
        fmt(str): target image type
    Returns:
        bytes: the image converted to `fmt` type
    """
    webp_image_bytes = base64.b64decode(base64_webp_str)

    with BytesIO(webp_image_bytes) as webp_stream:
        webp = Image.open(webp_stream)
        with BytesIO() as out:
            webp.save(out, fmt)
            return out.getvalue()
