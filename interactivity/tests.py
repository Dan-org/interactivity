"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from pyamf.remoting.client import RemotingService
import logging


class GatewayTest(TestCase):

    def test_gateway_available(self):
        '''
        Tests to make sure we can connect to the gateway
        '''
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
        )
        gw = RemotingService('http://127.0.0.1:8000/interactivity/', logger=logging)
        service = gw.getService('interactivity')
        output = service.hello()
        #print output
        self.assertEqual(1,1)
        


	

