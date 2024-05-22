import requests
from bs4 import BeautifulSoup
import re


sentences = format_data(team1)
def get_wiki_page(params):
    return requests.get('https://en.wikipedia.org/w/api.php', params=params)


def get_NCAA_D1_teams():
    params = {
        'action': 'parse',
        'page': "List of NCAA Division I institutions",
        'format': 'json',
        'prop': 'text',
    }
    res = get_wiki_page(params)
    if res.status_code == 200:
        page = res.json()['parse']['text']['*']
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find_all('table')[1]
        team_names = []
        for row in table.find_all('tr')[2:]:
            cells = row.find_all('td')
            if len(cells) < 3:
                continue
            nickname = cells[2].find('a')['title']
            team_names.append(nickname)
    return team_names


def get_team_data(team_name):
    params = {
        'action': 'query',
        'titles': team_name,
        'format': 'json',
        'prop': 'extracts',
        'explaintext': 'true',
    }
    res = get_wiki_page(params)
    pages = res.json()['query']['pages']
    if pages:
        data = pages[next(iter(pages))]['extract']
        return format_data(data)
    

def format_data(data):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', data)
    sentences = list(filter(None, map(str.strip, sentences)))

    for sentence in sentences:
        print(sentence)
    return sentences