import requests
import ConfigParser

from sys import argv


def get_search_response_itemId (sr):
    try:
        return sr['items'][0]['itemId']
    except:
        raise Exception('No items returned')


def get_product_ids(p, n):
    # returns a list of up to the first n item ids
    try:
        return map(lambda x: x['itemId'], p[:n])
    except:
        raise Exception('No recommended products')


def product_ratings(iids, api_key, n):
    # Returns a sorted list of up to n product ids with average rating.  Products without reviews are assigned -1
    try:
        rating = []
        for i in iids:
            query = 'http://api.walmartlabs.com/v1/reviews/%s?apiKey=%s&format=json' % (i,api_key)
            r = requests.get(query).json().get('reviewStatistics',None)
            avg_rating = -1
            if r is not None:
                avg_rating = float(r['averageOverallRating'])
            rating.append((i, avg_rating))
        rating.sort(key=lambda x: -x[1])
        return rating[:n]
    except:
        raise Exception('product_ratings failed')


def main(argv):
    try:
        if len(argv) == 1:
            raise Exception('No query specified')
        q = argv[1]
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        api_key = config.get('Section1','api_key')

        search_q = 'http://api.walmartlabs.com/v1/search?apiKey=%s&query=%s&numItems=1&format=json' % (api_key,q)
        iid = get_search_response_itemId(requests.get(search_q).json())
        print "First item id: %s" % iid

        pr_q = 'http://api.walmartlabs.com/v1/nbp?apiKey=%s&itemId=%s&format=json' % (api_key, iid)
        ids = get_product_ids(requests.get(pr_q).json(), 10)

        ratings = product_ratings(ids, api_key, 10)

        result = " Here are the results: "
        for i in ratings:
            result += "\n %s %s " % (i[0],i[1])
        result += " %d" % len(ids)
        print result
    except Exception, err:
        print "Oops %s " % err.message

if __name__ == '__main__':
    main(argv)