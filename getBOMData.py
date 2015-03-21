import requests
from bs4 import BeautifulSoup
import csv

class GetBOMWeekendData(object):
	"""Collects methods/attributes for retrieving weekend data from Box Office Mojo."""

	def __init__(self, start_year, end_year):
		self.start_year = start_year
		self.end_year = end_year
		self.data = [self.get_weekend_gross_data(y) for y in xrange(start_year, end_year + 1)]

	def get_weekend_gross_data(self, year):
		year_data = []
		page_soup = BeautifulSoup(requests.get('http://www.boxofficemojo.com/weekend/?yr={0}&p=.htm'.format(year)).content)
		table_rows = page_soup('table')[4].findAll('tr')
		for i in xrange(1, len(table_rows)):
			row = table_rows[i]
			tds = row('td')
			td_strings = [year] + [tds[td_i].string.encode('utf8') for td_i in xrange(len(tds))]
			year_data.append(td_strings)
		return year_data

	def get_data(self):
		return self.data

class GetBOMWeeklyData(object):
	"""Collects methods/attributes for retrieving weekly data from Box Office Mojo."""

	def __init__(self, start_year, end_year):
		self.start_year = start_year
		self.end_year = end_year
		self.data = [self.get_weekend_gross_data(y) for y in xrange(start_year, end_year + 1)]

	def get_weekend_gross_data(self, year):
		year_data = []
		page_soup = BeautifulSoup(requests.get('http://www.boxofficemojo.com/weekly/?yr={0}&p=.htm'.format(year)).content)
		table_rows = page_soup('table')[3].findAll('tr')
		for i in xrange(1, len(table_rows)):
			row = table_rows[i]
			tds = row('td')
			td_strings = [year] + [tds[td_i].string.encode('utf8') for td_i in xrange(len(tds))]
			year_data.append(td_strings)
		return year_data

	def get_data(self):
		return self.data

data = GetBOMWeeklyData(1999, 2015).get_data()
print data

with open('weekly_box_office_since_1999.csv', 'w') as f:
	writer = csv.writer(f)
	for year in data:
		writer.writerows(year)

class AnalyzeBOMWeekendData(object):
	"""Analyzes the data from the GetBOMWeekendData class."""

	def __init__(self):
		with open('test.csv', 'rU') as f:
			reader = csv.reader(f)
			self.data = [row for row in reader]
	
	def get_avg_pct(self):
		years = xrange(1982, 2015)
		self.year_avg = {}

		for year in years:
			year_data = filter(lambda x: x[0] == str(year), self.data)
			avg_pct = reduce(lambda x, y: x + float(y[9][:-1]), year_data, 0) / len(year_data)
			self.year_avg[year] = avg_pct

		return self.year_avg

	def get_top_5_min(self):
		top_5_min_dict = {}
		years = xrange(1982, 2015)
		for year in years:
			year_data = filter(lambda x: x[0] == str(year), self.data)
			top_5_min = sorted(year_data, key=lambda row: float(row[9][:-1]))
			top_5_min_dict[year] = map(lambda row: int(row[8]), top_5_min)
		return top_5_min_dict

# analysis = AnalyzeBOMWeekendData()
# top_5_min = analysis.get_top_5_min()

# for year in analysis.get_top_5_min():
# 	print year, top_5_min[year]