import requests
from bs4 import BeautifulSoup as bs
import re

def crawl_station():
    headers = {
        'Referer': 'http://www.seoulmetro.co.kr/kr/cyberStation.do?menuIdx=538',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'http://www.seoulmetro.co.kr/kr/getLineData.do', headers=headers, verify=False)

    soup = bs(response.text, "html.parser")

    linename = re.compile('{}(.*){}'.format(re.escape('"data-label" : "'),
                        re.escape('"'))).findall(response.text)
    stname = re.compile('{}|{}(.*){}'.format(re.escape('"data-label" : "'),
                        re.escape('"station-nm": "'), re.escape('"'))).findall(response.text)
    del stname[0]

    stname.append("")

    stations = {}
    for i in range(len(linename)):
        line = []

        while True:
            if stname[0] == "":
                del stname[0]
                break
            line.append(stname[0].replace("\\n", " "))
            del stname[0]

        stations[linename[i]] = line
    
    return stations
