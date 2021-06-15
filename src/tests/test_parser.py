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

    def test_extract_sensor_dataframe(self):
        # Load the correct data df
        load_path = "./test_files/test_df_correct.csv"
        correct_df = pd.read_csv(load_path, index_col=0)
        correct_data_df = pd.DataFrame(ast.literal_eval(correct_df["data"][0]))

        # Load test df and test extract_sensor_dataframe function
        # txt file first
        path = "test_files/temp.txt"
        df = parser.get_latest_frame(path)
        data_txt_df = parser.extract_sensor_dataframe(df)

        assert_frame_equal(correct_data_df, data_txt_df)

        # csv file
        path = "test_files/test_df_correct.csv"
        df = pd.read_csv(path, index_col=0)
        data_csv_df = parser.extract_sensor_dataframe(df)

        assert_frame_equal(correct_data_df, data_csv_df)




