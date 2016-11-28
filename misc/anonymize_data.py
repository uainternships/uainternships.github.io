import csv
import os
import base64
import hashlib


SALT_BITS = 32

def anonymize_data(rows):
    result = {}
    for row in rows:
        # Get relevant fields
        email = row['Email Address']
        completeness = row['Application completeness']
        eligibility_language = row['Eligibility (language)']
        eligibility_education = row['Eligibility (education)']
        qualification = row['Qualification']
        eligibility_integral = row['Eligibility (integral)']
        resume_readiness = row['Resume readiness']

        # Clean data
        qualification = qualification in ['FAIR', 'GOOD', 'EXCELLENT']
        eligibility_language = eligibility_language == 'ELIGIBLE'
        eligibility_education = eligibility_education in \
                ['ELIGIBLE', 'NOT ELIGIBLE FOR SOME POSITIONS', 'MAYBE ELIGIBLE']
        completeness = completeness == 'COMPLETE'
        eligibility_integral = eligibility_integral == 'TRUE'

        # Compile anonymized data
        h = hashlib.sha256(email.encode('utf-8')).hexdigest()
        anonymized_item = {
            'qualification': qualification,
            'language': eligibility_language,
            'education': eligibility_education,
            'completeness': completeness,
            'eligibility': eligibility_integral,
        }
        result[h] = anonymized_item
    return result


if __name__ == '__main__':
    import sys
    import json
    csv_path = sys.argv[1]
    with open(csv_path) as handle:
        reader = csv.DictReader(handle)
        anonymized = anonymize_data(reader)
        print(json.dumps(anonymized))

