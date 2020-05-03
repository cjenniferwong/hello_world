from typing import Iterable

from .. import models
from ..resources import db
from ..jennwong_files import Services, get_summary


# These two functions should be the limit of your interaction with the ORM in this part
# of the challenge, other than constructing result rows.


def read_all_rows(model_class):
    """ Given a model class, return all rows in the db of that model """
    session = db.make_session()
    return session.query(model_class).all()


def write_summary_rows(summary_rows: Iterable[models.PythonSolutionRow]):
    """ Write a collection of summary rows to the database. """
    session = db.make_session()
    session.add_all(summary_rows)
    session.commit()


def create_analysis_table():
    """ Implement the logic to read from DB write final table"""

    # TODO!
    claim_dict = {claim.id: [claim.date, claim.patient_id] for claim in read_all_rows(models.Claim)}
    patient_dict = {patient.id: patient.birth_date for patient in read_all_rows(models.Patient)}

    service_list = []
    for service_line in read_all_rows(models.ServiceLine):
        claim_date, patient_id = claim_dict[service_line.claim_id]
        patient_birthdate = patient_dict[patient_id]
        service = Services(service_line.id, service_line.primary_diag_code,
                           claim_date, patient_id, patient_birthdate)
        service_list.append(service)

    code_dict = get_summary(service_list)

    summary_rows = []

    for code, age_bracket_dict in code_dict.items():
        for age_bracket, patient_list in age_bracket_dict.items():
            summary_row = models.PythonSolutionRow(
                primary_diag_code=code, age_bracket=age_bracket, num_unique_patients=len(set(patient_list)))
            summary_rows.append(summary_row)

    # Example writing dummy answer row
    write_summary_rows([
        models.PythonSolutionRow(
            primary_diag_code="1234.56",
            age_bracket="0-4",
            num_unique_patients=123
        )
    ])

    write_summary_rows(summary_rows)
