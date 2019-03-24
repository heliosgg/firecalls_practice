import json
import re

import matplotlib.pyplot as plt
import requests

from secret_key import api_key

dataset_id = '1950'
link = 'https://apidata.mos.ru/v1/datasets/' + dataset_id + '/rows?api_key=' + api_key

response = requests.get(link)
data = response.text

month_count = {
    'январь' : 0,
    'февраль' : 0,
    'март' : 0,
    'апрель' : 0,
    'май' : 0,
    'июнь' : 0,
    'июль' : 0,
    'август' : 0,
    'сентябрь' : 0,
    'октябрь' : 0,
    'ноябрь' : 0,
    'декабрь' : 0,
}

year_count = {}

regex_month = re.compile(r'([А-Яа-яЁё]+)\s(\d{1,4})')

for record in json.loads(data):
    month_year = regex_month.match(record['Cells']['MonthReport'])
    month = month_year.group(1).lower()
    year = int(month_year.group(2))

    month_count[month] += int(record['Cells']['Calls'])

    if year not in year_count.keys():
        year_count[year] = 0
    year_count[year] += 1

unique_years = len(year_count)

max_calls = 0.0
max_calls_iter = 0
i = 0

for k, v in month_count.items():
    month_count[k] /= unique_years

    if max_calls < month_count[k]:
        max_calls = month_count[k]
        max_calls_iter = i
    i += 1

min_calls = max_calls
min_calls_iter = 0
i = 0

for k, v in month_count.items():
    if min_calls > v:
        min_calls = v
        min_calls_iter = i
    i += 1

plt.figure(figsize=(12,5))
ax = plt.gca()

ax.set_facecolor('#1e1e1e')

plt.grid(color='w', linestyle='--', linewidth=0.45, zorder=0)
bars = plt.bar(list(month_count.keys()), month_count.values(), color='#d0d000', zorder=3)
bars[max_calls_iter].set_color('#d00000')
bars[min_calls_iter].set_color('#00d000')

plt.ylim(bottom=min_calls - 200)
plt.ylim(top=max_calls + 100)

plt.xlabel('месяцы')
plt.ylabel('количество вызовов')
plt.savefig('result.png', dpi = 300)
plt.show()

print(month_count)
