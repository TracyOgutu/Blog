import urllib.request,json
from . model import Quote

quote_url=None

def configure_request(app):

    global quote_url
    quote_url = app.config['QUOTE_URL']


def get_quotes():

    get_quotes_url = quote_url

    print('********quoteurl***********')
    print(get_quotes_url)

    with urllib.request.urlopen(get_quotes_url) as url:

          
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)


        quotes_results = None

        if get_quotes_response['quote']:
            quotes_results_list = get_quotes_response['quote']
            quotes_results = quotes_results_list

    return quotes_results


