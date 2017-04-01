import urllib.request
import json

def getProductNumbers():
    productList = []

    # Go through pages until all products found
    for page in range(1, 3):
        url = "https://msi.bbycastatic.ca/mobile-si/si/v3/products/search?query=*&storeId&zipCode&facetsOnly&platform&lang=en&page={}"\
                .format(page)
        text = urllib.request.urlopen(url)
        jsonText = json.load(text)

        documentsArray = jsonText['searchApi']['documents']

        for doc in documentsArray:
            productList.append(doc['skuId'])

    print(productList)

getProductNumbers()

# count = 0
# for productNumber in range(10415309, 10415320):
#
#     url = "https://msi.bbycastatic.ca/mobile-si/si/v4/pdp/overview/{}?lang=en"\
#             .format(productNumber)
#     text = urllib.request.urlopen(url)
#
#     if text.contains("<!DOCTYPE"):
#         continue
#     j = json.load(text)
#     print(j)
#
#
# print(count)

    # print (j['productId'])
    # response = j['si']['response']
    #
    # print(response)