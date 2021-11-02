"""
Create a csv file with fake data
id,userid,country,city,campaign,payment
"""
import random
import csv

ROWS = 100
countries = ['UA', 'EU', 'UK', "US"]
countries_and_cities = {
    'UA': ['CV', 'KYV', 'LV', "KHA"],
    'EU': ['BAR', 'PAR', 'MAD', 'WR'],
    'UK': ['LND', 'MAN'],
    'US': ['NY', "WA", 'AU']
}
campaignes = ['internship', 'full work', 'part work']

result = []
for row in range(ROWS):
    id_ = row
    userid = 100 + id_
    country = countries[random.randrange(0, len(countries))]
    cities = countries_and_cities[country]
    city = cities[random.randrange(0, len(cities))]
    campaign = campaignes[random.randrange(0, len(campaignes))]
    payment = round(random.random(), 2)

    print(f'{id_}, {userid}, {country}, {city}, {campaign}, {payment}')
    result.append([id_, userid, country, city, campaign, payment])


with open('test_input.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['id', 'userid', 'country', 'city', 'campaign', 'payment'])
    csv_writer.writerows(result)
