from django.test import TestCase
from rest_framework.request import Request
from rest_framework.response import Response
from vcfapi.views import VCFView
from django.http import HttpRequest, QueryDict
from saphetor.settings import VCF_TEST_FILE
from vcfapi.vcfreader import VCFReader
import json
# Create your tests here.

class VCFApiTestcase(TestCase):
    '''
    def setUp(self) -> None:
        VCFReader(VCF_TEST_FILE)
    '''
    def test_get_single_record(self):
        res = self.client.get('/vcfapi/records/?id=rs62635284')
        self.assertEqual(res.status_code, 200)
        expected_data = {
            "CHROM":'chr1',
            "POS": '12783',
            "ID": 'rs62635284',
            "REF": 'G',
            "ALT": 'A',
        }
        self.assertEqual(json.loads(res.content), expected_data)

    def test_get_record_not_found(self):
        res = self.client.get('/vcfapi/records/?id=rs6263528')
        expected_data = 'Record not found'
        self.assertEqual(json.loads(res.content), expected_data)

    def test_delete_record(self):
        header = {'HTTP_AUTHORIZATION': 'Basic test'}
        res = self.client.delete('/vcfapi/records/?id=rs626352876', data='', content_type='', **header)
        self.assertEqual(res.status_code, 204)
        expected_data = ''
        self.assertEqual(res.content.decode(), expected_data)
        res = self.client.get('/vcfapi/records/?id=rs626352876')
        expected_data = 'Record not found'
        self.assertEqual(json.loads(res.content), expected_data)
    
    def test_delete_record_not_authorized(self):
        res = self.client.delete('/vcfapi/records/?id=rs62635284')
        self.assertEqual(res.status_code, 403)
        expected_data = {"detail":"Authentication credentials were not provided."}
        self.assertEqual(json.loads(res.content.decode()), expected_data)

    def test_insert_record(self):
        insert_data = {
            "CHROM":'chr1',
            "POS": '12783',
            "ID": 'rs62635',
            "REF": 'A',
            "ALT": 'A',
        }
        header = {'HTTP_AUTHORIZATION': 'Basic test'}
        res = self.client.post('/vcfapi/records/', data=insert_data, content_type='application/json', **header)
        self.assertEqual(res.status_code, 201)
        expected_data = ''
        self.assertEqual(res.content.decode(), expected_data)
        res = self.client.get('/vcfapi/records/?id=rs62635')
        self.assertEqual(json.loads(res.content), insert_data)

    def test_edit_record(self):
        res = self.client.get('/vcfapi/records/?id=rs369820305')
        edit_data = {
            "CHROM":'chr1',
            "POS": '12783',
            "ID": 'rs369820305',
            "REF": 'A',
            "ALT": 'A',
        }
        self.assertNotEqual(json.loads(res.content), edit_data)
        header = {'HTTP_AUTHORIZATION': 'Basic test'}
        res = self.client.put('/vcfapi/records/?id=rs369820305', data=edit_data, content_type='application/json', **header)
        self.assertEqual(res.status_code, 200)
        expected_data = ''
        self.assertEqual(res.content.decode(), expected_data)
        res = self.client.get('/vcfapi/records/?id=rs369820305')
        self.assertEqual(json.loads(res.content), edit_data)