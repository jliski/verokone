#!/usr/bin/env python

import scraperwiki
import lxml.html


def handle_person_year(year_row_tr, name, birthyear):
    tds = year_row_tr.cssselect("td")

    if len(tds) == 10:
        year = int(tds[0].text_content())
        print '    Handling year: %d' % year
        data = {
            'nimi' : name,
            'syntymavuosi' : int(birthyear),
            'vuosi' : year,
            'asema' : tds[1].text_content(),
            'kokonaistulot' : float((tds[2].text_content()).replace(",",".")),
            'ansiotulot' : float((tds[4].text_content()).replace(",",".")),
            'paaomatulot' : float((tds[5].text_content()).replace(",",".")),
            'varallisuus' : (tds[6].text_content()).replace(",","."),
            'veroprosentti' : float((tds[7].text_content()).replace("%","")),
            'sij_kokonaistulot' : (tds[8].text_content()),
            'sij_ansiotulot' : (tds[9].text_content())
        }
        unique_keys=['vuosi'] + ['nimi'] + ['syntymavuosi']
        scraperwiki.sql.save(unique_keys, data=data)
    else:
        raise Exception('Check this guy, something else than 10 tds')

def handle_person(person_link, birthyear):
    url = 'http://www.hs.fi/%s' % person_link 
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    name = root.cssselect("div[class='taxperson-center'] h2")[0].text
    print '  Handling %s' % name + ' (syntynyt: ' + birthyear + ').'
    all_rows = root.cssselect("div[class='tax-person-yearlist'] tr")
    all_except_header = all_rows[1:]
    for year_row_tr in all_except_header:
        handle_person_year(year_row_tr, name, birthyear)


def handle_year(year):
    print 'Handling year = %d' % i
    url = 'http://www.hs.fi/verokone/haku/?nimi=&ika=%d-%d&maakunta=&sukupuoli=&asema=&vuosi=2012&laaja=true' % (i, i)
    # hakusivu antaa max. 500 tulosta, eli suurimmissa ikaluokissa haettava erikseen esim. miehet ja naiset
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for person_link in root.xpath('//td[@class="details-cell"]/a'):
        birthyear = person_link.attrib['href'][18:22]
        handle_person(person_link.attrib['href'], birthyear)
        

# Let's start
for i in range(0,30): # tahan ei kovin isoa valia tai kestaa ikuisuuden
    handle_year(i)
