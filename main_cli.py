import requests
import ConfigParser
import time

from sys import argv

def rate_limited(max_per_second):
    min_interval = 1.0 / float(max_per_second)
    def decorate(func):
        last_time_called = [0.0]
        def rate_limited_function(*args, **kargs):
            elapsed = time.clock() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kargs)
            last_time_called[0] = time.clock()
            return ret
        return rate_limited_function
    return decorate


@rate_limited(5)  # 5 per second at most
def query_walmart_api(q):
    return requests.get(q)


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
    # Returns a sorted list of up to n product ids with average rating.
    #   Products without reviews are assigned -1
    try:
        rating = []
        for i in iids:
            query = \
                'http://api.walmartlabs.com/v1/reviews/%s?apiKey=%s&format=json' % (i,api_key)
            r = query_walmart_api(query).json().get('reviewStatistics',None)
            avg_rating = -1
            if r is not None:
                avg_rating = float(r['averageOverallRating'])
            rating.append((i, avg_rating))
        rating.sort(key=lambda x: -x[1])
        return rating[:n]
    except:
        raise Exception('product_ratings failed')


def hello_world(q):
    #Searches for products based upon a user-provided search string
    #Uses the first item in the search response to query the product recommendation search
    #Retrieves 10 product recommendations
    #Returns the fetched product recommendations order by average customer review
    try:
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        api_key = config.get('Section1','api_key')
        search_q = 'http://api.walmartlabs.com/v1/search?apiKey=%s&query=%s&numItems=1&format=json' % (api_key,q)

        iid = get_search_response_itemId(query_walmart_api(search_q).json())
        print "First item id: %s" % iid

        pr_q = 'http://api.walmartlabs.com/v1/nbp?apiKey=%s&itemId=%s&format=json' % (api_key, iid)
        ids = get_product_ids(query_walmart_api(pr_q).json(), 10)

        ratings = product_ratings(ids, api_key, 10)

        result = " Here are %d recommended products, ranked by average customer review: " % len(ids)
        for i in ratings:
            result += "\n %s %s " % (i[0],i[1])
        result += " \nn = %d" % len(ids)
        print result
        return len(ids)
    except Exception, err:
        print "Oops %s " % err.message
        return err.message


if __name__ == '__main__':
    if len(argv) == 1:
        raise Exception('No query specified')
    hello_world(argv[1])