from vcfapi.vcfreader import VCFReader, OutOfBounds, VCFRecordNotFound
from vcfapi.serializers import VCFSerializer
from abc import abstractmethod
from rest_framework.request import Request

class NotImplemented(Exception):
    pass


class RecordNotFound(Exception):
    pass

class OutOfLimits(Exception):
    pass

class BadParameters(Exception):
    pass

class Usecase:
    def __init__(self, request: Request) -> None:
        self.request = request

    @abstractmethod
    def get_data(self):
        raise NotImplemented('Not Implemented')
    
    @property
    def response(self) -> dict:
        return self.get_data()

class GetRecord(Usecase):
    def get_data(self) -> dict:
        try:
            #id from url params
            id = self.request.query_params.get('id')
            #get record with id from vcf file
            vcf_rec, ofs, sz = VCFReader().get_vcf_record(id)
            #serialize to json
            data = VCFSerializer.serialize(vcf_rec)
            return data
        except VCFRecordNotFound as e:
            raise RecordNotFound('Record not found')
        

class GetRecordList(Usecase):
    def get_data(self) -> dict:
        try:
            # default ofs is the first record
            ofs = int(self.request.query_params.get('ofs')) if self.request.query_params.get('ofs') else 0
            # default size is 10 records
            size = int(self.request.query_params.get('size')) if self.request.query_params.get('size') else 10
            # check for invalid offeset and size values
            if ofs < 0 or size < 1:
                raise BadParameters('Negative offset')
            
            # get list of records from vcf file
            raw_recs = VCFReader().get_record_list(ofs, size)
            recs = [VCFSerializer.serialize(vcf_rec) for vcf_rec in raw_recs ]
            return recs
        except OutOfBounds as e:
            raise OutOfLimits(str(e))

class InsertRecord(Usecase):
    def get_data(self):
        try:
            # json to vcf file string format
            vcf_rec = VCFSerializer().deserialize(self.request.data)
            VCFReader().insert_vcf_record(vcf_rec)
            return {}
        except VCFRecordNotFound as e:
            raise RecordNotFound('Record not found')

class DeleteRecord(Usecase):
    def get_data(self):
        try:
            id = self.request.query_params.get('id')
            # delete record with id from vcf file
            VCFReader().delete_vcf_record(id)
            return {}
        except VCFRecordNotFound as e:
            raise RecordNotFound('Record not found')

class EditRecord(Usecase):
    def get_data(self):
        try:
            rec = self.request.data
            id = rec['ID']
            vcf_rec = VCFSerializer().deserialize(rec)
            VCFReader().edit_vcf_record(id, vcf_rec)
            return {}
        except VCFRecordNotFound as e:
            raise RecordNotFound('Record not found')
