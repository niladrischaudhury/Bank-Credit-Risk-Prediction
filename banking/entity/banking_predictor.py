import os
import sys

from banking.exception import BankingException
from banking.util.util import load_object

import pandas as pd


class BankingData:

    def __init__(self,
                 status: int,
                 duration: int,
                 credit_history: int,
                 purpose: int,
                 amount: int,
                 savings: int,
                 employment_duration: int,
                 installment_rate: int,
                 personal_status_sex: int,
                 other_debtors: int,
                 present_residence: int,
                 property: int,
                 age: int,
                 other_installment_plans: int,
                 housing: int,
                 number_credits: int,
                 job: int,
                 people_liable: int,
                 telephone: int,
                 foreign_worker: int,
                 credit_risk: int = None
                 ):
        try:
            self.status = status
            self.duration = duration
            self.credit_history = credit_history
            self.purpose = purpose
            self.amount = amount
            self.savings = savings
            self.employment_duration = employment_duration
            self.installment_rate = installment_rate
            self.personal_status_sex = personal_status_sex
            self.other_debtors = other_debtors
            self.present_residence = present_residence
            self.property = property
            self.age = age
            self.other_installment_plans = other_installment_plans
            self.housing = housing
            self.number_credits = number_credits
            self.job = job
            self.people_liable = people_liable
            self.telephone = telephone
            self.foreign_worker = foreign_worker
            self.credit_risk = credit_risk
        except Exception as e:
            raise BankingException(e, sys) from e

    def get_banking_input_data_frame(self):

        try:
            banking_input_dict = self.get_banking_data_as_dict()
            return pd.DataFrame(banking_input_dict)
        except Exception as e:
            raise BankingException(e, sys) from e

    def get_banking_data_as_dict(self):
        try:
            input_data = {
                "status": [self.status],
                "duration": [self.duration],
                "credit_history": [self.credit_history],
                "purpose": [self.purpose],
                "amount": [self.amount],
                "savings": [self.savings],
                "employment_duration": [self.employment_duration],
                "installment_rate": [self.installment_rate],
                "personal_status_sex": [self.personal_status_sex],
                "other_debtors": [self.other_debtors],
                "present_residence": [self.present_residence],
                "property": [self.property],
                "age": [self.age],
                "other_installment_plans": [self.other_installment_plans],
                "housing": [self.housing],
                "number_credits": [self.number_credits],
                "job": [self.job],
                "people_liable": [self.people_liable],
                "telephone": [self.telephone],
                "foreign_worker": [self.foreign_worker]}
            return input_data
        except Exception as e:
            raise BankingException(e, sys)


class BankingPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise BankingException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise BankingException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            credit_risk = model.predict(X)
            return credit_risk
        except Exception as e:
            raise BankingException(e, sys) from e