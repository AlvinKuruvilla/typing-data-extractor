from td_data_dict import TD_Data_Dictionary, make_dataframe
import datapane as dp
import os


class DataReporter:
    def __init__(self, report_dir_path=os.path.join(os.getcwd(), "reports")):
        self.report_dir_path = report_dir_path

    def tabulate_td_data_dict(self, data_dict: TD_Data_Dictionary):
        df = make_dataframe(data_dict)
        print(dp.Table(df))
        return dp.DataTable(df)

    def get_report_path(self):
        return self.report_dir_path

    def set_report_path(self, path):
        self.report_dir_path = path
