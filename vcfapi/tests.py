from django.test import TestCase
from rest_framework.request import Request
from rest_framework.response import Response
from vcfapi.views import VCFView
from django.http import HttpRequest, QueryDict
from saphetor.settings import VCF_TEST_FILE
from vcfapi.vcfreader import VCFReader
from vcfapi import usecases
import json, os
from unittest.mock import MagicMock, patch
# Create your tests here.

class VCFApiTestcase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_file = 'test_data.vcf'
        with open(cls.test_file, 'a+') as vcf_file:
            line1= """
            ##fileformat=VCFv4.2
            ##reference=/ref/genomes/hg19/hg19.fa
            ##FILTER=<ID=FAIL,Description="SNV quality < 100 or indel quality < 100 or DP < 8">        
            #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA12877 single 20180302
            chr1	12783	rs62635284	G	A	99.03	FAIL	AC=2;AF=1;AN=2;DANN_score=0.275765;DP=4;ExcessHet=3.0103;FS=0;Gene=DDX11L1,LOC102725121;MLEAC=2;MLEAF=1;MQ=27;QD=24.76;SOR=3.258;function=intronic;gnomadGenomesAC=13919;gnomadGenomesAN=24922;gnomadGenomes_AC_Hom=1519;gnomadGenomes_AF=0.559451	GT:AB:AD:DP:GQ:PL:SAC	./.:1:0,4:4:12:127,12,0:0,0,4,0
            chr1	13116	rs626352876	T	G	736.77	PASS	AC=1;AF=0.5;AN=2;BaseQRankSum=3.42;ClippingRankSum=0;DANN_score=0.25605;DP=27;ExcessHet=3.0103;FS=1.819;Gene=DDX11L1,LOC102725121;MLEAC=1;MLEAF=0.5;MQ=29.87;MQRankSum=-3.415;QD=27.29;ReadPosRankSum=1.551;SOR=1.329;function=intronic;gnomadGenomesAC=15410;gnomadGenomesAN=28466;gnomadGenomes_AC_Hom=1783;gnomadGenomes_AF=0.542246	GT:AB:AD:DP:GQ:PL:SAC	0/1:0.703704:8,19:27:99:765,0,361:3,5,5,14
            chr1	13118	rs62028691	A	G	736.77	PASS	AC=1;AF=0.5;AN=2;BaseQRankSum=0.966;ClippingRankSum=0;DANN_score=0.317087;DP=26;ExcessHet=3.0103;FS=0;Gene=DDX11L1,LOC102725121;MLEAC=1;MLEAF=0.5;MQ=29.19;MQRankSum=-3.167;QD=28.34;ReadPosRankSum=1.114;SOR=0.941;function=intronic;gnomadGenomesAC=15338;gnomadGenomesAN=28396;gnomadGenomes_AC_Hom=1779;gnomadGenomes_AF=0.541135	GT:AB:AD:DP:GQ:PL:SAC	0/1:0.730769:7,19:26:99:765,0,361:2,5,5,14
            chr1	13656	rs1263393206	CAG	C	196.73	PASS	AC=1;AF=0.5;AN=2;BaseQRankSum=-3.067;ClippingRankSum=.;DP=12;ExcessHet=3.0103;FS=0;Gene=DDX11L1,LOC102725121;MLEAC=1;MLEAF=0.5;MQ=24.17;MQRankSum=-0.825;QD=16.39;ReadPosRankSum=0.307;SOR=0.693;function=non-coding exon,intronic,splicing,splicing-ACMG;gnomadExomes_AC=670;gnomadExomes_AC_Hemi=0;gnomadExomes_AC_Hom=20;gnomadExomes_AF=0.0295331;gnomadExomes_AN=23940;gnomadGenomesAC=13044;gnomadGenomesAN=26616;gnomadGenomes_AC_Hom=99;gnomadGenomes_AF=0.489766	GT:AB:AD:DP:GQ:PL:SAC	0/1:0.5:6,6:12:99:234,0,260:1,5,1,5
            chr1	62186	.	G	T	62.74	FAIL	AC=2;AF=1;AN=2;DANN_score=0.740699;DP=2;ExcessHet=3.0103;FS=0;MLEAC=2;MLEAF=1;MQ=47;QD=31.37;SOR=0.693	GT:AB:AD:DP:GQ:PL:SAC	./.:1:0,2:2:6:90,6,0:0,0,1,1
            chr1	62203	rs28402963	T	C	62.74	FAIL	AC=2;AF=1;AN=2;DANN_score=0.225532;DP=2;ExcessHet=3.0103;FS=0;MLEAC=2;MLEAF=1;MQ=47;QD=31.37;SOR=0.693;gnomadGenomesAC=8434;gnomadGenomesAN=21178;gnomadGenomes_AC_Hom=1154;gnomadGenomes_AF=0.401422	GT:AB:AD:DP:GQ:PL:SAC	./.:1:0,2:2:6:90,6,0:0,0,1,1
            chr1	131281	rs1263932941	C	G	52.77	FAIL	AC=1;AF=0.5;AN=2;BaseQRankSum=-1.834;ClippingRankSum=.;DANN_score=0.521882;DP=6;ExcessHet=3.0103;FS=11.761;Gene=CICP27,ENSG00000238009;MLEAC=1;MLEAF=0.5;MQ=20.69;MQRankSum=-1.834;QD=8.79;ReadPosRankSum=1.834;SOR=3.223;function=non-coding exon,intronic;gnomadGenomesAC=867;gnomadGenomesAN=8572;gnomadGenomes_AC_Hom=0;gnomadGenomes_AF=0.0971149	GT:AB:AD:DP:GQ:PL:SAC	./.:0.666667:2,4:6:35:81,0,35:2,0,0,4
            chr1	131310	rs1198932538	G	C	71.03	FAIL	AC=2;AF=1;AN=2;DANN_score=0.547746;DP=4;ExcessHet=3.0103;FS=0;Gene=CICP27,ENSG00000238009;MLEAC=2;MLEAF=1;MQ=20;QD=17.76;SOR=3.258;function=non-coding exon,intronic;gnomadGenomesAC=1206;gnomadGenomesAN=6822;gnomadGenomes_AC_Hom=2;gnomadGenomes_AF=0.17158	GT:AB:AD:DP:GQ:PL:SAC	./.:1:0,4:4:12:99,12,0:0,0,0,4
            chr1	133483	rs369820305	G	T	216.77	PASS	AC=1;AF=0.5;AN=2;BaseQRankSum=1.445;ClippingRankSum=0;DANN_score=0.590411;DP=24;ExcessHet=3.0103;FS=1.674;Gene=CICP27,ENSG00000238009;MLEAC=1;MLEAF=0.5;MQ=24.19;MQRankSum=0;QD=9.03;ReadPosRankSum=-1.165;SOR=1.445;function=non-coding exon;gnomadGenomesAC=8915;gnomadGenomesAN=28168;gnomadGenomes_AC_Hom=662;gnomadGenomes_AF=0.316528	GT:AB:AD:DP:GQ:PL:SAC	0/1:0.5:12,12:24:99:245,0,244:6,6,4,8
            """
            vcf_file.write(line1)
        cls.reader = VCFReader('test_data.vcf')


    def test_get_single_record(self):
        with patch('vcfapi.usecases.VCFReader', return_value=self.reader) as mocked_reader:
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
        with patch('vcfapi.usecases.VCFReader', return_value=self.reader) as mocked_reader:
            res = self.client.get('/vcfapi/records/?id=rs6263528')
        
            expected_data = 'Record not found'
            self.assertEqual(json.loads(res.content), expected_data)

    def test_delete_record(self):
        with patch('vcfapi.usecases.VCFReader', return_value=self.reader) as mocked_reader:
            header = {'HTTP_AUTHORIZATION': 'Basic test'}
            res = self.client.delete('/vcfapi/records/?id=rs626352876', data='', content_type='', **header)
            self.assertEqual(res.status_code, 204)
            expected_data = ''
            self.assertEqual(res.content.decode(), expected_data)
            res = self.client.get('/vcfapi/records/?id=rs626352876')
            expected_data = 'Record not found'
            self.assertEqual(json.loads(res.content), expected_data)
    
    def test_delete_record_not_authorized(self):
        with patch('vcfapi.usecases.VCFReader', return_value=self.reader) as mocked_reader:
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
        with patch('vcfapi.usecases.VCFReader', return_value=self.reader) as mocked_reader:
            res = self.client.post('/vcfapi/records/', data=insert_data, content_type='application/json', **header)
            self.assertEqual(res.status_code, 201)
            expected_data = ''
            self.assertEqual(res.content.decode(), expected_data)
            res = self.client.get('/vcfapi/records/?id=rs62635')
            self.assertEqual(json.loads(res.content), insert_data)

    def test_edit_record(self):
        with patch('vcfapi.usecases.VCFReader', return_value=self.reader) as mocked_reader:
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
    
    @classmethod
    def tearDownClass(cls):
        cls.reader.unmap()
        os.remove(cls.test_file)