import pytest
import os
from app.utils.file_reader.csv_file_reader import CSVFileReader

TEST_CSV_FILE = 'test_large_csv_file.csv'

SAMPLE_DATA = '''Name,Age
Alice,25
Bob,30
Charlie,22
'''

@pytest.fixture
def create_test_csv_file():
    with open(TEST_CSV_FILE, 'w') as file:
        file.write(SAMPLE_DATA)


def test_read_csv_as_dict(create_test_csv_file):
    reader = CSVFileReader(TEST_CSV_FILE)

    data_dict = reader.read_csv_as_dict()

    expected_data = [{'Name': 'Alice', 'Age': '25'},
                    {'Name': 'Bob', 'Age': '30'},
                    {'Name': 'Charlie', 'Age': '22'}]

    assert data_dict == expected_data


def test_non_existent_file():
    non_existent_file = 'non_existent_file.csv'
    reader = CSVFileReader(non_existent_file)
    with pytest.raises(FileNotFoundError):
        reader.read_csv_as_dict()


def test_clean_up():
    if os.path.exists(TEST_CSV_FILE):
        os.remove(TEST_CSV_FILE)
