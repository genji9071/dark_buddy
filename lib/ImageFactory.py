import base64
import uuid
from io import BytesIO

from PIL import Image

from config import redis


class ImageFactory():
    def get_image_by_uuid(self, uuid):
        bytes_image = redis.get(self.get_redis_key(uuid))
        if bytes_image is None:
            return ''
        bytes_image = self.base64_to_image(bytes_image.decode())
        return bytes_image

    def get_redis_key(self, uuid):
        return 'tianhao:dark_buddy:image_factory:{0}'.format(uuid)

    def put_image_by_uuid(self, image):
        id = uuid.uuid1()
        data = self.image_to_base64(image)
        redis.setex(name=self.get_redis_key(id), time=300,
                    value=data)
        return id

    @staticmethod
    def image_to_base64(img):
        output_buffer = BytesIO()
        img.save(output_buffer, format="png")
        byte_data = output_buffer.getvalue()
        return base64.b64encode(byte_data)

    @staticmethod
    def base64_to_image(base64_str):
        byte_data = base64.b64decode(base64_str)
        image_data = BytesIO(byte_data)
        return Image.open(image_data)


image_factory = ImageFactory()
