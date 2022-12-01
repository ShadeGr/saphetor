import mmap
from saphetor.settings import VCF_FILE

class ReaderSingleton(object):
    
    _instance = None

    def __new__(cls, fname='', *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class OutOfBounds(Exception):
    pass

class VCFRecordNotFound(Exception):
    pass

class VCFReader(ReaderSingleton):
    def __init__(self, fname='') -> None:
        if fname == '':
            fname = VCF_FILE
        with open(fname, 'a+') as vc_file:
            #Map file with write access rights
            mapped_file = mmap.mmap(vc_file.fileno(), 0, access=mmap.ACCESS_WRITE)
            start_pos = 0
            #find offset where actual data begins
            while True:
                line = mapped_file.readline()
                if line.startswith(b'#'):
                    start_pos = mapped_file.tell()
                    continue

                self.start_data_pos = start_pos
                break
        
        self.mfile = mapped_file

    def load_file(self, fname):
        with open(fname, 'a+') as vc_file:
            #Map file with write access rights
            mapped_file = mmap.mmap(vc_file.fileno(), 0, access=mmap.ACCESS_WRITE)
            start_pos = 0
            #find offset where actual data begins
            while True:
                line = mapped_file.readline()
                if line.startswith(b'#'):
                    start_pos = mapped_file.tell()
                    continue

                self.start_data_pos = start_pos
                break
        
        self.mfile = mapped_file
    def get_vcf_record(self, id):
        #Place locator at start of the actual data
        self.mfile.seek(self.start_data_pos)
        #search for id
        rec_pos = self.mfile.find(b'\t' + id.encode() + b'\t')
        if rec_pos == -1:
           raise VCFRecordNotFound('record not found')
        #place locator at the start of the line containing the requested id
        while self.mfile[rec_pos] != ord('\n'):
            rec_pos -= 1
        rec_pos += 1
        self.mfile.seek(rec_pos)

        #read and return record and offset of the requested record
        record = self.mfile.readline()
        return record, rec_pos, len(record)

    def get_record_list(self, offset, size):
        self.mfile.seek(self.start_data_pos)
        recs = []
        #error if offset < 0
        if offset < 0:
            raise OutOfBounds("offset out of bounds")
        
        #skip till offset
        while offset > 0:
            line = self.mfile.readline()
            if not line or line == '':
                raise OutOfBounds("offset out of bounds")
            
            offset-= 1
        
        #read up to <size> records
        while size > 0:
            line = self.mfile.readline()
            if line == '' or not line:
                break
            recs.append(line)
            size-= 1
        return recs


    def delete_vcf_record(self, id):
        #find record to delete
        record, rec_pos, rec_size = self.get_vcf_record(id)        
        #get current size of file
        total_size = self.mfile.size()
        #calculate size of data after the requested record
        move_size = total_size - rec_pos - rec_size
        #print('file size before delete: ' + str(total_size))
        
        #copy rest of data on top of the record that we want to delete
        self.mfile.move(rec_pos, (rec_pos + rec_size), move_size)
        self.mfile.flush()
        #resize file to new size
        self.mfile.resize(total_size - rec_size)
        #print('file size after delete: ' + str(self.mfile.size()))

    def insert_vcf_record(self, rec):
        #Calculate new size of file including new record
        old_end = self.mfile.size()
        self.mfile.resize(self.mfile.size() + len(rec.encode()) + 1)
        #Place file locator at the end of the file
        self.mfile.seek(old_end)
        #append new rec
        self.mfile.write(rec.encode() + b'\n')
        self.mfile.flush()

    def edit_vcf_record(self, id, new_rec):
        #Get offset of the record to be edited
        new_rec = new_rec.encode() + b'\n'
        record, rec_pos, rec_size = self.get_vcf_record(id)
        diff_size = len(new_rec) - rec_size

        #Calculate differential size between old and new record. needed for resizing file
        new_size = self.mfile.size() + diff_size
        #print('Old size: ' + str(self.mfile.size()) + ' New size: ' + str(new_size))
        #Calculate data size of all records after the one to be edited (old_rec)
        move_size = self.mfile.size() - rec_pos - rec_size

        #if new record is bigger than old, resize file first
        if diff_size > 0:
            self.mfile.resize(new_size + 1)
        
        #Copy all data after old record to new offset. New offset is the start of the line of the old record + length of the new record.
        self.mfile.move(rec_pos+len(new_rec), rec_pos + rec_size, move_size)
        #place file locator at the start of the old record
        self.mfile.seek(rec_pos)
        #write new record in place of the old one
        self.mfile.write(new_rec)
        self.mfile.flush()


        if diff_size < 0:
            self.mfile.resize(new_size)
        
        
