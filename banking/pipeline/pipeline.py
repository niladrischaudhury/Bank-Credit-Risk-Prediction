from tkinter import E
from sklearn.pipeline import Pipeline
from banking.config.configuration import Configuartion
from banking.logger import logging
from banking.exception import BankingException

from banking.entity.artifact_entity import DataIngestionArtifact
from banking.entity.config_entity import DataIngestionConfig
from banking.component.data_ingestion import DataIngestion

import os, sys

class Pipeline:

    def __init__(self, config: Configuartion = Configuartion()) -> None:
        try:
            self.config = config

        except Exception as e:
            raise BankingException(e, sys) from e

    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config.get_data_ingestion_config())

            data_ingestion.initiate_data_ingestion()
        
        except Exception as e:
            raise BankingException(e, sys) from e
