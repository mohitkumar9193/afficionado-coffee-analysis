"""Verified public educational source, distinct from Afficionado records."""
import hashlib
import io
import zipfile
from pathlib import Path
from urllib.request import urlopen
import pandas as pd

SOURCE_URL = 'https://maven-datasets.s3.amazonaws.com/Coffee+Shop+Sales/Coffee+Shop+Sales.zip'
SOURCE_PAGE = 'https://mavenanalytics.io/data-playground/coffee-shop-sales'
SOURCE_SHA256 = 'be13c59c4cfdc0d1b08ceab514aea50a0cd329c916e4c3585eeef92a5b4c3a2c'


def read_public_archive(content):
    if hashlib.sha256(content).hexdigest() != SOURCE_SHA256:
        raise ValueError('Public source changed. Revalidate the dataset before analysis.')
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        workbook = archive.read('Coffee Shop Sales.xlsx')
    return pd.read_excel(io.BytesIO(workbook), sheet_name='Transactions', dtype=str,
                         keep_default_na=False, engine='openpyxl')


def load_public_data():
    bundled = Path(__file__).resolve().parents[1] / 'data/public/maven-coffee-transactions.csv.gz'
    if bundled.exists():
        content = bundled.read_bytes()
        if hashlib.sha256(content).hexdigest() != 'e5de8d073fd865b14a8053b7307c3f492a0b9a13ccc316ca8176a404a992e20c':
            raise ValueError('Bundled case-study data checksum failed.')
        return pd.read_csv(io.BytesIO(content), compression='gzip', dtype=str, keep_default_na=False)
    with urlopen(SOURCE_URL, timeout=45) as response:
        return read_public_archive(response.read())

