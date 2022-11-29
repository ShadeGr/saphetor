from vcfapi.vcfreader import VCFReader, OutOfBounds, VCFRecordNotFound
from django.http import JsonResponse, HttpResponseNotFound
from vcfapi.serializers import VCFSerializer
from rest_framework.exceptions import NotFound
from abc import ABC, abstractmethod

class NotImplemented(Exception):
    pass


class RecordNotFound(Exception):
    pass

class OutOfLimits(Exception):
    pass

class Usecase(ABC):
    @abstractmethod
    def get_data(self):
        raise NotImplemented('Not Implemented')
    
    @property
    def response(self) -> dict:
        return self.get_data()

class GetRecord(Usecase):

    def __init__(self, id):
        self.id = id
        super().__init__()
    def get_data(self):
        try:
            vcf_rec, ofs, sz = VCFReader().get_vcf_record(self.id)
            data = VCFSerializer.serialize(vcf_rec)
            return data
        except VCFRecordNotFound as e:
            raise RecordNotFound('Record not found')
        

class GetRecordList(Usecase):

    def __init__(self, ofs=0, sz=10):
        self.offset = ofs
        self.size = sz
        super().__init__()
    def get_data(self) -> dict:
        try:
            if self.offset < 0:
                raise OutOfLimits('Negative offset')
            raw_recs = VCFReader().get_record_list(self.offset, self.size)
            recs = [VCFSerializer.serialize(vcf_rec) for vcf_rec in raw_recs ]
            return recs
        except OutOfBounds as e:
            raise OutOfLimits(str(e))

class InsertRecord(Usecase):
    
    def __init__(self, data):
        self.data = data
        super().__init__()
    
    def get_data(self):
        try:
            vcf_rec = VCFSerializer().deserialize(self.data)
            VCFReader().insert_vcf_record(vcf_rec)
            return {}
        except VCFRecordNotFound as e:
            raise RecordNotFound('Record not found')

class DeleteRecord(Usecase):
    
    def __init__(self, id):
        self.id = id
        super().__init__()
    
    def get_data(self):
        try:
            VCFReader().delete_vcf_record(self.id)
            return {}
        except VCFRecordNotFound as e:
            print('eeee')
            raise RecordNotFound('Record not found')