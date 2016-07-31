import requests
from flask import Flask, request

app = Flask(__name__)


def create_search_string(req):
    #This function creates a search query for the Walmart search API.  It raises an exception if
    #query is not present but does not validate that other parameters are valid
    api_key =  req.args.get('api_key')
    if not api_key:
        raise Exception('No API key provided!')
    q = req.args.get('query')
    if q:
        s = 'http://api.walmartlabs.com/v1/search?apiKey=%s&query=%s&numItems=1&format=json' % (api_key,q)

        sort = req.args.get('sort')
        if sort:
            s = '%s&sort=%s' % (s, sort)

        order = req.args.get('order')
        if order:
            s = '%s&order=%s' % (s,order)

        start = req.args.get('start')
        if start:
            s = '%s&start=%s' % (s, start)

        categoryId = req.args.get('categoryId')
        if categoryId:
            s = '%s&categoryId=%s' % (s, categoryId)

        facet = req.args.get('facet')
        if facet:
            s = '%s&facet=%s' % (s, facet)

        ff = req.args.get('facet.filter')
        if ff:
            s = '%s&facet.filter=%s' % (s, ff)

        fr = req.args.get('facet.range')
        if fr:
            s = '%s&facet.range=%s' % (s,fr)

        return (s, api_key)

    else:
        raise Exception('No Query.  ')

def get_search_response_itemId (sr):
    try:
        return sr['items'][0]['itemId']
    except:
        raise Exception('No items returned')


def get_product_ids(p, n):
    # returns a list of up to the first n item ids
    try:
        #return map(lambda x : get_item_id(x) ,p[:n])
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


@app.route('/')
def hello_world():
    iid = 'None'
    try:
        search_q, api_key = create_search_string(request)
        iid = get_search_response_itemId(requests.get(search_q).json())

        pr_q = 'http://api.walmartlabs.com/v1/nbp?apiKey=%s&itemId=%s&format=json' % (api_key, iid)
        ids = get_product_ids(requests.get(pr_q).json(), 10)

        ratings = product_ratings(ids, api_key, 10)

        result = " Here are the results: "
        for i in ratings:
            result += " %s %s " % (i[0],i[1])
        result += " %d" % len(ids)
        return result
    except Exception, err:
        return "Oops %s First product response %s " % (err.message, iid)

if __name__ == '__main__':
    app.run()