import os
import requests
import urllib.request
from bs4 import BeautifulSoup

LINE_NOTIFY_TOKEN = '<YOUR TOKEN>'


def get_csv():
    saitama_url = 'https://www.pref.saitama.lg.jp/a0701/covid19/jokyo.html'
    res = requests.get(saitama_url)

    soup = BeautifulSoup(res.content, 'lxml')
    href = soup.select('a[href$="csv"]')
    csv_url = ['https://www.pref.saitama.lg.jp' + _["href"] for _ in href]
    csv_file = os.path.basename(csv_url[0])
    urllib.request.urlretrieve(csv_url[0], f'/tmp/{csv_file}')

    with open(f'/tmp/{csv_file}', encoding='shift-jis', newline='') as f:
        rows = [row for row in f]
        return rows[0].split(','), rows[-1:][0].split(',')


def line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = {'message': message}
    requests.post(url, headers=headers, data=data)


def main():
    csv_header, csv_record = get_csv()
    info = dict(zip(csv_header, csv_record))

    message = (
        info[list(info.keys())[0]] + '\n'
        '・' + list(info.keys())[1] + '\n\t' + info[list(info.keys())[1]] + '\n'
        '・' + list(info.keys())[2] + '\n\t' + info[list(info.keys())[2]] + '\n'
        '・' + list(info.keys())[3] + '\n\t' + info[list(info.keys())[3]] + '\n'
        '・' + list(info.keys())[4] + '\t' + info[list(info.keys())[4]]
    )
    line_notify(message)


if __name__ == "__main__":
    main()
