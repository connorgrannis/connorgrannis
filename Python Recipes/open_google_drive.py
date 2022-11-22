from PIL import Image
import pandas as pd
from io import BytesIO
from urllib.request import urlopen

def format_url(link):
    id = link.split('/')[-2]
    url = f"https://drive.google.com/uc?export=downloads&id={id}"
    my_file = BytesIO(urlopen(url).read())


def open_google_drive(link, data_type="table"):
  if data_type.lower()[:3] == "img":
    return Image.open(format_url(link))
  elif data_type.lower() == "table":
    return pd.read_csv(format_url(link))
  else:
    return None
