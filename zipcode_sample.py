# zipcode_sample_download.py

import os
import csv
from typing import Dict, Iterator, Tuple
from urllib.request import urlretrieve
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

def get_code_and_name_from_csv(zipcode_csv_path: str) -> Iterator[Tuple[str, str]]:
    """CSV 파일에서 우편번호, 시도, 시군구, 도로명을 읽어서, 우편번호와 주소를 생성합니다.
    :param zipcode_csv_path: 우편번호 CSV 파일 경로
    :return: 우편번호, 주소 튜플을 생성(yield)합니다.
    """

    with open(zipcode_csv_path, "rt", encoding="utf-8-sig") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter="|")  # DictReader를 사용하면 첫 줄을 컬럼명으로 자동 처리합니다. 우편번호 CSV 파일은 구분자가 | 입니다.
        row: Dict
        for row in csv_reader:
            code = row["우편번호"]
            name = "{시도} {시군구} {도로명}".format(**row)
            yield code, name

def main():
    csv_path = "shop/asset/zipcode_DB/서울특별시.txt"  

    generator = get_code_and_name_from_csv(csv_path)

    print(next(generator))  # 처음 1줄을 가져옵니다.
    print(next(generator))  # 다음 1줄을 가져옵니다.
    print(next(generator))  # 다음 1줄을 가져옵니다.

if __name__ == "__main__":
    main()