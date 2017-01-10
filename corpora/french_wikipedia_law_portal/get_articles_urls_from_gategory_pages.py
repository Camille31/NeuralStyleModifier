"""
For each gategory url in category_pages_urls.txt, get the corresponding web page and save
all unique article urls in articles_urls.txt
"""

import codecs
import sys
import os
from sets import Set
import urllib2
from bs4 import BeautifulSoup

url_prefix = "https://fr.wikipedia.org"
input_file_path = "category_pages_urls.txt"
output_file_path = "articles_urls.txt"

articles_urls = Set()

def read_category_pages_urls_file():
	category_pages_urls = []
	with open(input_file_path) as category_pages_urls_file:
		category_pages_urls = category_pages_urls_file.read().splitlines()
	return category_pages_urls

def get_articles_urls_from_category_page(category_page_url):
	category_page_url = url_prefix + category_page_url
	category_page = urllib2.urlopen(category_page_url).read()
	category_page_soup = BeautifulSoup(category_page, "lxml")
	category_page_soup.prettify()
	for anchor in category_page_soup.select('#mw-pages .mw-content-ltr a'):
		print anchor['href']
		articles_urls.add(anchor['href'])

def write_articles_urls_to_output_file():
	print "write_articles_urls_to_output_file"
	with codecs.open(output_file_path, 'w', encoding='utf8') as articles_urls_file:
		for articles_url in articles_urls:
			articles_urls_file.write(articles_url + os.linesep)

def main(argv):
	category_pages_urls = read_category_pages_urls_file()
	for id_cat, category_page_url in enumerate(category_pages_urls):
		print id_cat
		get_articles_urls_from_category_page(category_page_url)
		if id_cat > 10:
			break
	write_articles_urls_to_output_file()

if __name__ == "__main__":
	main(sys.argv[1:])
