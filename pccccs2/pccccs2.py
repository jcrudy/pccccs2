import csv
import os
from .resources import resources
from clinvoc.icd9 import ICD9PCS, ICD9CM
from clinvoc.icd10 import ICD10CM, ICD10PCS
import pickle
from clinvoc.code_collections import CodeCollection
from ._version import get_versions
from . import __version__
from six import next
# icd9_corrections = {'81.09': None,
#                     '06.88': '996.88',
#                     '428.83': None}
# icd10_correction = {}

def _read_file(filename):
    try:
        with open(os.path.join(resources, 'cache.pickle'), 'rb') as infile:
            result, v = pickle.load(infile)
        assert v == __version__
        assert not get_versions()['dirty']
        return result
    except:
        icd9cm_expanded_vocab = ICD9CM(use_decimals=True)
        icd9pcs_vocab = ICD9PCS(use_decimals=True)
        icd9mixed_vocab = ICD9CM(use_decimals=True) | ICD9PCS(use_decimals=True)
        icd10cm_vocab = ICD10CM(use_decimals=True)
        icd10pcs_vocab = ICD10PCS(use_decimals=True)
        icd10mixed_vocab = ICD10CM(use_decimals=True) | ICD10PCS(use_decimals=False)
        result = {}
        with open(filename, 'rt') as infile:
            reader = csv.reader(infile)
            next(reader)
            for row in reader:
                if row[3].strip().replace('/', '').upper() != 'NA':
                    all_codes = icd9mixed_vocab.parse(row[3])
                    result[(row[1], row[2], icd9cm_expanded_vocab.vocab_domain, icd9cm_expanded_vocab.vocab_name)] = icd9cm_expanded_vocab.filter(all_codes)
                    result[(row[1], row[2], icd9pcs_vocab.vocab_domain, icd9pcs_vocab.vocab_name)] = icd9pcs_vocab.filter(all_codes)
    #                 res = (all_codes) - (result[(row[1], row[2], 'icd9cm')] | result[(row[1], row[2], 'icd9pcs')])
    #                 if res:
    #                     print 'icd9:', res
                if row[4].strip().replace('/', '').upper() != 'NA':
                    all_codes = icd10mixed_vocab.parse(row[4])
                    result[(row[1], row[2], icd10cm_vocab.vocab_domain, icd10cm_vocab.vocab_name)] = icd10cm_vocab.filter(all_codes)
                    result[(row[1], row[2], icd10pcs_vocab.vocab_domain, icd10pcs_vocab.vocab_name)] = icd10pcs_vocab.filter(all_codes)
    #                 res = (all_codes) - (result[(row[1], row[2], 'icd10cm')] | result[(row[1], row[2], 'icd10pcs')])
    #                 if res:
    #                     print 'icd10:', res
        with open(os.path.join(resources, 'cache.pickle'), 'wb') as outfile:
            pickle.dump((result, __version__), outfile)
        return result

# try:
#     with open(os.path.join(resources, 'cache.pickle'), 'rb') as infile:
#         _code_sets = pickle.load(infile)
# except:
#     _code_sets = _read_file(os.path.join(resources, 'extracted_codes.csv'))
#     with open(os.path.join(resources, 'cache.pickle'), 'wb') as outfile:
#         pickle.dump(_code_sets, outfile)

code_sets = CodeCollection(*_read_file(os.path.join(resources, 'extracted_codes.csv')).items(), 
                           name='pcccs2', levels=['category', 'subcategory', 'domain', 'vocabulary'])

