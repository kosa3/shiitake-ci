import json

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

CONSTELLATIONS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]

BASE_URL = "https://voguegirl.jp/horoscope/shiitake/"


def main():
    # 今週の月曜日(ciで回すから月曜の指定はどちらでもいい)
    now = datetime.now()
    monday = (now - relativedelta(days=now.weekday())).strftime("%Y%m%d")
    output_data = {}
    for constellation in CONSTELLATIONS:
        # https://voguegirl.jp/horoscope/shiitake/taurus/20200601/
        url = f'{BASE_URL}{constellation}/{monday}/'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, features="html.parser")
        response.close()

        analysis = soup.find("div", class_="a-text")
        advice = analysis.find_next("div", class_="a-text")
        power_up = soup.find("dd", class_="o-recommend-color__dd")
        cool_down = power_up.find_next("dd", class_="o-recommend-color__dd")

        output_data[constellation] = {}
        output_data[constellation].update([
            ("analysis", analysis.get_text().strip()),
            ("advice", advice.get_text().strip()),
            ("power_up", power_up.get_text().strip()),
            ("cool_down", cool_down.get_text().strip()),
        ])

    # jsonデータ生成
    f = open(f'{monday}.json', 'w')
    json.dump(output_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
