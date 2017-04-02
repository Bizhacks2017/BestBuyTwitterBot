import urllib.request
import json

PRODUCTS_PER_PAGE = 96
PAGES_PER_WRITE = 20
TOTAL_PAGES_OF_CATALOG = 25
MIN_REVIEW_LENGTH = 30

# Gets the total number of products
def getTotalNumberOfProducts():
    url = "https://msi.bbycastatic.ca/mobile-si/si/v3/products/search?query=*&storeId&zipCode&facetsOnly&platform&lang=en&page=1"
    text = urllib.request.urlopen(url)
    jsonText= json.load(text)

    return jsonText['searchApi']['num_found']

# Gets the SKU numbers of all the products
def getProductNumbers():
    productList = []
    totalNumberOfProducts = getTotalNumberOfProducts()

    with open("sku.txt", 'w') as outfile:
        # Do something
        outfile.write("")

    # Go through pages until all products found
    for page in range(1, TOTAL_PAGES_OF_CATALOG):
        print ("Working on page " + str(page))
        url = "https://msi.bbycastatic.ca/mobile-si/si/v3/products/search?query=*&storeId&zipCode&facetsOnly&platform&lang=en&page={}&rows={}"\
                .format(page, PRODUCTS_PER_PAGE)
        text = urllib.request.urlopen(url)
        jsonText = json.load(text)

        # Array that contains the list of products
        documentsArray = jsonText['searchApi']['documents']

        # Get all product sku's on  a page
        for doc in documentsArray:
            sku = doc['skuId']
            # Some fake id's started with an M. Filter those
            if sku[0] != "M":
                productList.append(doc['skuId'])

        # Write to file in batches so list doesn't get too big
        if page % PAGES_PER_WRITE == 0:
            print("Writing to file")

            # Write id's to a file
            with open("sku.txt", 'a') as outfile:
                for sku in productList:
                    line = sku + '\n'
                    outfile.write(line)

            # Empty list
            productList = []

        if (page * PRODUCTS_PER_PAGE) >= totalNumberOfProducts:
            break

    # Write id's to a file
    with open("sku.txt", 'a') as outfile:
        for sku in  productList:
            line = sku + '\n'
            outfile.write(line)

    print ("There were " +  str(TOTAL_PAGES_OF_CATALOG * PRODUCTS_PER_PAGE)  + " products in the product")

def getAllProductReviews():
    shortReviewCount = 0
    productsWithReviews = 0
    numberOfReviews = 0
    currentLineOfFile = 0

    with open("sku.txt") as infile:
        for line in infile:
            currentLineOfFile += 1

            if currentLineOfFile < 1320:
                continue

            if currentLineOfFile %10 == 0:
                print("Count: " + str(currentLineOfFile))
                print("There were " + str(numberOfReviews) + " total reviews")
                print("There were " + str(shortReviewCount) + " reviews with less that " + str(
                    MIN_REVIEW_LENGTH) + " characters")
                print("There were " + str(productsWithReviews) + " products with reviews")
            # if currentLineOfFile >= 100:
            #     break

            # Get product reviews
            reviews = getProductReviews(str(line)[:-1])

            # Check if there are no reviews for the product
            if len(reviews) == 0:
                continue
            productsWithReviews += 1

            # Process reviews
            for review in reviews:
                text = review['reviewText']
                if (len(text) == 0):
                    print("Review text was empty")
                    continue

                numberOfReviews += 1
                if len(text) < MIN_REVIEW_LENGTH:
                    shortReviewCount += 1

    print("There were " + str(numberOfReviews) + " total reviews")
    print("There were " + str(shortReviewCount) + " reviews with less that " + str(MIN_REVIEW_LENGTH) + " characters")
    print("There were " + str(productsWithReviews) +  " products with reviews")
    return shortReviewCount


def getProductReviews( skuId ):
    url = "https://msi.bbycastatic.ca/mobile-si/si/pdp/reviewDetails/{}?lang=en&source=can"\
            .format(skuId)

    try:
        text = urllib.request.urlopen(url)
        jsonText = json.load(text)
        return jsonText['si']['response']['results']
    except Exception:
        return []


# Get all the sku numbers
# getProductNumbers()
getAllProductReviews()
