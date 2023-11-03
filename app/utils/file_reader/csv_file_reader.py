from typing import List, Dict

import pandas as pd
import logging


class CSVFileReader:
    def __init__(self, file_path: str, logger=None):
        self.file_path = file_path
        self.logger = logger if logger else logging.getLogger(__name__)

    def read_csv_as_dict(self) -> List[Dict]:
        try:
            data_df = pd.read_csv(self.file_path, dtype='str')
            data_dict = data_df.to_dict(orient='records')
            return data_dict
        except FileNotFoundError:
            self.logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            raise e
