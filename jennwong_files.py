import datetime

'''
created a class to store attributes and methods to get the age of the patient at the time of the claim
'''


class Services:
    def __init__(self, service_line_id, primary_diag_code, claim_date, patient_id, patient_birth_date):
        self.service_line_id = service_line_id
        self.primary_diag_code = primary_diag_code
        self.claim_date = None
        self.set_claim_date(claim_date)
        self.patient_id = patient_id
        self.patient_birth_date = None
        self.set_patient_birth_date(patient_birth_date)

    def set_claim_date(self, value):
        self.claim_date = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        return self.claim_date

    def set_patient_birth_date(self, value):
        try:
            self.patient_birth_date = datetime.datetime.strptime(value, '%Y/%b/%d').date()
        # look into raise value exception
        except Exception as e:
            self.patient_birth_date = 'invalid_birthdate'
        return self.patient_birth_date

    def get_age(self):
        '''
        return the floor of the age bracket division
        '''
        age = (self.claim_date - self.patient_birth_date).days//365.25
        return age

    def get_age_bracket(self):
        '''
        we know that the brackets are in 5 year intervals
        find the top and bottom of the years lived
        '''
        if not isinstance(self.patient_birth_date, datetime.date):
            return 'invalid_birth_date'
        elif self.claim_date < self.patient_birth_date:
            return 'claim_date_before_birth_date'
        else:
            age = self.get_age()
            lower_bound = age // 5
            upper_bound = lower_bound + 1

        # note that the upperbound is exclusive so need to subtract 1
            bracket = str(int(lower_bound*5)) + '-' + str(int(upper_bound*5-1))
            return bracket


def get_summary(query_results):
    '''
    pass the results from querying the database for service lines
    returns a dictionary with code as keys and another [nested] dict for age brackets as value
    example:
    {code:
        {age_bracket: [patient_id_list]
        }
    }
    '''
    summary_dict = {}
    for service in query_results:
        code = service.primary_diag_code
        age_bracket = service.get_age_bracket()
        patient_id = service.patient_id

        # probably a better way to do this....
        summary_dict[code] = summary_dict.get(code, {})
        summary_dict[code][age_bracket] = summary_dict[code].get(age_bracket, [])
        summary_dict[code][age_bracket].append(patient_id)

        # to make sure its unique
        summary_dict[code][age_bracket] = list(set(summary_dict[code][age_bracket]))
    return summary_dict
