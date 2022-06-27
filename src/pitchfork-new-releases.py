#!/usr/bin/env python

from bs4 import BeautifulSoup


with open('temp/pitchfork-new.html') as doc:
    soup = BeautifulSoup(doc, 'html.parser')

with open('pitchfork-new-parsed.txt', 'a') as doc:
    for h in soup.find_all('div', {'class': 'body__inner-container'}):
        doc.write(h.find('h2').text)
        doc.write('\n')
        for p in h.find_all('p'):
            doc.write(p.text)
            doc.write('\n')


