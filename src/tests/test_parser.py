import io
import ast
from src.file import parser
from unittest import TestCase
import pandas as pd
from pandas._testing import assert_frame_equal
import os


class Test(TestCase):
    def test_get_latest_frame(self):
        load_path = "./test_files/test_df_correct.csv"
        path = "test_files/temp.txt"
        correct_df = pd.read_csv(load_path, index_col=0)
        correct_data_df = parser.extract_sensor_dataframe(correct_df)

        df = parser.get_latest_frame(path)
        data_df = parser.extract_sensor_dataframe(df)
        assert_frame_equal(correct_data_df, data_df)

    def test_save_file(self):
        load_path = "test_files/test_df_correct.csv"
        save_path = "../../transfer_data/test_df_correct.csv"
        df = pd.read_csv(load_path, index_col=0)
        df.to_csv(save_path)
        isFile = os.path.isfile(save_path)
        os.remove(save_path)
        assert(isFile)



