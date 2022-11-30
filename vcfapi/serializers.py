class VCFSerializer:
    @classmethod
    def serialize(cls, vcf_data: bytearray) -> dict:
        json_rec = {
            "CHROM":'',
            "POS": '',
            "ID": '',
            "REF": '',
            "ALT": '',
        }

        rec_list  = vcf_data.decode().strip().split('\t')
        key_list = list(json_rec.keys())
        for idx, item in enumerate(key_list):
            json_rec[item] = rec_list[idx]
        return json_rec

       
    @classmethod
    def deserialize(cls, data: dict) -> bytearray:
        vcf_rec = '{CHROM}\t{POS}\t{ID}\t{REF}\t{ALT}'.format(CHROM=data['CHROM'], POS=data['POS'], ID=data['ID'], REF=data['REF'], ALT=data['ALT'])
        return vcf_rec