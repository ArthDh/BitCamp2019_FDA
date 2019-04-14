from bs4 import BeautifulSoup
import urllib.request
import re
import pickle
from string import ascii_lowercase

src = 'http://www.finra.org/industry/individuals-barred-finra-'


barred_brokers = dict()
for c in ascii_lowercase:
    url = src + c
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table')

    for child in table.children:
        for td in child.children:
            crd_group = re.match(r"([0-9]+)", td.text, re.I)
            if crd_group:
                crd = crd_group.group()
                name = td.text[len(crd):]
                barred_brokers[crd] = name
                print(crd, " ", name)

print(len(barred_brokers))
path = "/Users/arth/Desktop/Finra/net/"
with open(path+'barred_brokers.pickle', 'wb') as file:
    pickle.dump(barred_brokers, file, protocol=pickle.HIGHEST_PROTOCOL)
