import os
import boto3
import uuid
import re
import pathlib
from scripts.mondrian.canvas import Canvas

key= os.environ.get('KEY_ID')
secret= os.environ.get('KEY_SECRET')

root = pathlib.Path(__file__).parent.resolve()

def aws_session(region_name='us-east-1'):
    return boto3.session.Session(aws_access_key_id=key,
                                aws_secret_access_key=secret,
                                region_name=region_name)


def upload_file_to_bucket(bucket_name, data):
    filename = str(uuid.uuid4())+'.svg'
    session = aws_session()
    s3_resource = session.resource('s3')
    object = s3_resource.Object(bucket_name, filename)
    object.put(Body=data,ACL='public-read', ContentType='image/svg+xml')

    s3_url = f"https://s3.amazonaws.com/{bucket_name}/{filename}"
    return s3_url

def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

if __name__ == '__main__':
    nlines = 12
    width, height = 200, 150
    minarea = 400 / (width * height)
    canvas = Canvas(width, height)
    urls = list()
    for i in range(3):
        import xml.dom.minidom
        canvas.make_painting(nlines, minarea)
        svg = canvas.get_svg()
        dom = xml.dom.minidom.parseString(svg)
        xml = dom.toxml()
        url = upload_file_to_bucket('bot.github', xml)
        urls.append(f'![mondrian_{i}]({url})')

    readme = root / "README.md"
    readme_contents = readme.open().read()
    md = "\n".join(urls)

    rewritten = replace_chunk(readme_contents, "art", md)
    readme.open("w").write(rewritten)
