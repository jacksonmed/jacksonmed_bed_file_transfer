import re
import pandas as pd
from datetime import datetime
import ast


# path = "../tests/test_files/temp.txt"
# save_path = "../tests/test_files/test_df_correct.csv"
# # save_path = "../../transfer_data/temp.txt"


def get_latest_frame(path):
    expression = "FRAME\s\d*\(psi\)\n"

    with open(path) as f:
        lines = f.read()
        temp = re.split(expression, lines)

        element = temp[-1]

        date = element.split("\n")[0]
        data = element.split(date + "\n")[1]
        data = re.sub('\n$', '', data)
        data = data.split("\n")
        data = [re.sub('\t$', '', list_element) for list_element in data]
        data = [list_element.split("\t") for list_element in data]

        date_time = datetime.now()

        final_df = pd.DataFrame.from_dict({date_time: [data]}, orient='index', columns=['data'])
    return final_df


def save_df_csv(df, path):
    df.to_csv(path)


def extract_sensor_dataframe(df):
    data = df["data"].iloc[0]
    if type(data) == str:
        data = ast.literal_eval(data)
    df = pd.DataFrame(data)
    return df
