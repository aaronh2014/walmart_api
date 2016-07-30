import requests
import ConfigParser

from sys import argv

def create_search_string(q,api_key):
    #This function creates a search query for the Walmart search API.
    s = 'http://api.walmartlabs.com/v1/search?apiKey=%s&query=%s&numItems=1&format=json' % (api_key,q)
    return s


def get_search_response(q):
    #Queries Walmart Search API
    try:
        sr = requests.get(q).json()
        return sr
    except:
        raise Exception('get_search_response failed')


def get_search_item(search_result,n):
    #This function takes a search response and provides the itemId of the nth response
    try:
        iid = get_item_id(search_result['items'][n])
        return iid
    except:
        raise Exception('get_search_item failed')


def get_item_id(r):
    # returns the itemId from a item response
    try:
        return r['itemId']
    except:
        raise Exception('No itemId')


def get_product_rec(iid,api_key):
    # queries the Walmart Product recommendation API
    try:
        pr_q = 'http://api.walmartlabs.com/v1/nbp?apiKey=%s&itemId=%s&format=json' % (api_key,iid)
        products = requests.get(pr_q).json()
        return products
    except:
        raise Exception('get_product_rec failed')


def get_product_ids(p, n):
    # returns a list of the first n item ids
    try:
        ids = []
        for i in p[:n]:
            ids.append(get_item_id(i))
        return ids
    except:
        raise Exception('No recommended products')


def get_product_review(iid,api_key):
    # queries Walmart Review Api
    try:
        query = 'http://api.walmartlabs.com/v1/reviews/%s?apiKey=%s&format=json' % (iid,api_key)
        return requests.get(query).json()
    except:
        raise Exception('get_product_review failed')


def product_ratings(iids, api_key, n):
    # Returns a sorted list of n product ids with average rating.  Products without reviews are at the bottom
    try:
        rating = []
        for i in iids:
            r = get_product_review(i,api_key).get('reviewStatistics',None)
            avg_rating = -1
            if r is not None:
                avg_rating = float(r['averageOverallRating'])
            rating.append((i, avg_rating))
        rating.sort(key=lambda x: -x[1])
        return rating[:n]
    except:
        raise Exception('product_ratings failed')


script, q = argv
config = ConfigParser.RawConfigParser()
config.read('config.ini')
api_key = config.get('Section1','api_key')

search_q = create_search_string(q,api_key)
search_response = get_search_response(search_q)
iid = get_search_item(search_response,0)

recs = get_product_rec(iid, api_key)
ids = get_product_ids(recs, 10)

ratings = product_ratings(ids, api_key, 10)

result = " Here are the results: "
for i in ratings:
    result += "\n %s %s " % (i[0],i[1])
result += " %d" % len(ids)
print result
