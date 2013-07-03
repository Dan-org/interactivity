from pyamf.remoting.client import RemotingService
import logging

def test_gateway():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
    )
    
    gw = RemotingService('http://127.0.0.1:8000/interactivity/', logger=logging)
    service = gw.getService('interactivity')
    print service.loadClientConfig()
    
    
def test_url():
    ###query_args = { 'q':'query string', 'foo':'bar' }
    #query_args = {}
    #encoded_args = urllib.urlencode(query_args)
    #print 'Encoded:', encoded_args

    url = 'http://127.0.0.1:8000/interactivity/'
    headers = {'Content-Type': 'application/x-amf', 'User-Agent': 'PyAMF/0.6.1'}

    post_data = [('name','Gladys'),]     # a sequence of two element tuples

    http_request = urllib2.Request(url, urllib.urlencode(post_data))#, headers) #self._root_url, body.getvalue(), self._get_execute_headers())
    fbh = urllib2.urlopen(http_request, encoded_args).read()
    
    
test_gateway()