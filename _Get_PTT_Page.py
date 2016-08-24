# Receives two arguments:
# the name of the forum board followed by number of documents we desire.
import requests, bs4, codecs, sys

def GetArticleFromPTTPage(pageLink):
	fullLink = 'https://www.ptt.cc' + pageLink
	res = requests.get(fullLink)
	soup = bs4.BeautifulSoup(res.text)
	elements = soup.select('#main-content')
	OutputTextFile(pageLink, elements)

def OutputTextFile(fileName, elements):
    # We take the substring of the input file name to get rid of ".html" and other unnecessary crap.
	file = codecs.open(fileName[11:-5] +'.txt','w','utf-8')
	for element in elements:
		file.write(element.getText())
	file.close()
	print('Completed download.' + '\n')

# Program starts here.
board = sys.argv[1]
maxPage = sys.argv[2]
print("You selected " + board + " board with maximum page " + maxPage)
currentPage = 0
while currentPage <= int(maxPage):
	print("Processing index page: " + str(currentPage))
	try:
		if currentPage == 0:
			urlLink = 'https://www.ptt.cc/bbs/' + board + '/index.html'
		else:
			urlLink = 'https://www.ptt.cc/bbs/' + board + '/index' + str(currentPage) + '.html'
		print(urlLink)
		res = requests.get(urlLink)
		if (res.status_code == 404):
			print("Page not found.")
		elif (res.status_code == 503):
			print("Error code 503: Service temporarily unavailable. Could be possible banning from the remote system.")
            # To make the script try again, we decrement the counter by 1, which would later be added 1.
			currentPage = currentPage - 1
		else:
			print("Index page exists.")
			res.raise_for_status()
			soup = bs4.BeautifulSoup(res.text)
			elements = soup.select('a')
            for element in elements:
                print("Retrieving PTT page:")
				print(element.getText().split())
				GetArticleFromPTTPage(element['href'])

	except Exception as exc:
		print("Error: %s" % exc)

	currentPage = currentPage + 1
