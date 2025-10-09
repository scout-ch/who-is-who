import json
import os
import boto3
from botocore.client import Config


s3 = boto3.client(
    "s3",
    endpoint_url=f"{os.environ['MINIO_URL']}",
    aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)
bucket_name = os.environ["MINIO_BUCKET"]


try:
    s3.head_bucket(Bucket=bucket_name)
except:
    s3.create_bucket(Bucket=bucket_name)


def upload_image(image, imagename):
    filename = imagename + os.path.splitext(image.filename)[1]
    s3.upload_fileobj(
        image, bucket_name, filename, ExtraArgs={"ContentType": image.content_type}
    )


def get_image(imagename):
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=imagename)
    if objects["KeyCount"] == 0:
        print("No keys found for {imagename}")
        return None
    return s3.get_object(Bucket=bucket_name, Key=objects["Contents"][0]["Key"])


def store(page, page_name, builddir="build"):
    filename = os.path.join(builddir, _filename(page_name, "html"))

    if not os.path.exists(builddir):
        os.makedirs(builddir)

    report = "replaced" if os.path.exists(filename) else "created"

    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(page)
        print(f"-- {report} {filename}")


def _filename(path, extension="html"):
    if path.split(".")[-1] != extension:
        path = ".".join([path, extension])
    return path


def store_to_json(data, filepath="transformed_data.json"):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
        )


def read_json(file):
    if not os.path.isfile(file):
        return {}

    with open(file, "r", encoding="utf-8") as file:
        return json.load(file)
