import requests as r
from bs4 import BeautifulSoup as b
from pprint import pprint

def _sort_news_by_votes(news_list):
    return sorted(news_list,key= lambda k: k['score'],reverse=True)

def _custom_news(links, subtext):
    news = []
    for ind,item in enumerate(links):
        title = links[ind].getText()
        href = links[ind].find('a')['href']
        score = subtext[ind].select('.score')
        if len(score):
            votes = int(score[0].getText().replace(' points','').replace(' point',''))
            if votes > 99:
                news.append({'title': title, 'link':href, 'score':votes})
    return _sort_news_by_votes(news)

def _main(source):
    res = r.get(source)
    if res.status_code == 200:
        soup = b(res.text, 'html.parser')
        links = soup.find_all('span', class_='titleline')
        subtext = soup.select('.subtext')
        pprint(_custom_news(links, subtext))
    else:
        print(f'Error fetching information, status code: {res.status_code}')

if __name__ == '__main__':
    sources = ['https://news.ycombinator.com/news','https://news.ycombinator.com/news?p=2']
    for i, source in enumerate(sources):
        if i == 0:
            print('---------------------PAGE 1---------------------')            
            _main(source)
        else:
            print('\n---------------------PAGE 2---------------------')
            _main(source)
    


