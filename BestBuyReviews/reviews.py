import urllib.request
import json

def getReviews(line):

    # empty list of reviews for a specific skuId
    reviewList = []

    # link for reviews related to skuId
    link = "https://msi.bbycastatic.ca/mobile-si/si/pdp/reviewDetails/{}"\
        .format(line)

    text = urllib.request.urlopen(link)
    jsonText = json.load(text)

    # numOfReviews = getNumberOfReviews(link)
    resultsArray = jsonText['si']['response']['results']

    print("Appending reviews for skuId: " + line)

    with open("reviews.txt", 'a') as outfile:
        for result in resultsArray:
            reviewText = result['reviewText']
            appenLline = reviewText + '\n'
            outfile.write(appenLline)


# file handle to read skuIds
fhandle = open("sku.txt", 'r')

#create the file if it doesn't exist
with open("reviews.txt", 'w') as outfile:
    outfile.write("")

for line in fhandle:
    getReviews(line)

print("All review successfully appended to file.")