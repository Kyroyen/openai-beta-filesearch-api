from openai import OpenAI
from django.conf import settings
from io import BytesIO
import tempfile

from openai.types.file_object import FileObject

def upload_bytesfile(bytestream, f_ext):
    client = OpenAI(
        # api_key=settings.OPENAI_API_KEY,
    )

    print("inside upload")

    bytestream.name = f_ext

    response = client.files.create(file = bytestream, purpose="assistants")


    return response
