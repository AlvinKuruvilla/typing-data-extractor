import os
import csv
import pandas as pd
from pathlib import Path
from rich.traceback import install

install()


class NoCSVFileError(Exception):
    """Exception raised if provided path is not a csv file.

    Attributes:
        path -- input path which caused the error
        message -- explanation of the error
    """

    def __init__(self, path, message):
        self.path = path
        self.message = message
        super().__init__(self.message)


def check_gen_dir():
    path = os.path.join(os.getcwd(), "testdata", "gen")
    if os.path.isdir(path):
        return
    else:
        os.mkdir(path)


def is_csv_file(path: str):
    is_file = os.path.isfile(os.path.join(os.getcwd(), "testdata", "bbmass", path))
    if is_file:

        # Now check that the extension is CSV
        if path.lower().endswith(".csv"):
            return True
        else:
            return False
    else:
        return False


class BBMASSConverter:
    def __init__(self, bbmass_dir_path: str):
        """
        Attributes:
        bbmass_dir_path -- the relative path to the directory containing all the bbmass files
        """
        self.bbmass_dir_path = bbmass_dir_path
        check_gen_dir()
        self.header = ["Press or Release", "Key", "Time"]
        pass

    def read(self, filename: str):
        # NOTE: The file name must be fully qualified with the file extension
        filepath = os.path.join(os.getcwd(), "testdata", self.bbmass_dir_path, filename)
        print("File: " + filepath)
        if is_csv_file(filepath):
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                _ = next(reader)  # Skips header
                rows = []
                for row in reader:
                    rows.append(row)
                return rows

    def get_bbmass_directory_path(self):
        return self.bbmass_dir_path

    def print_csv_file(self, filename):
        filepath = os.path.join(os.getcwd(), "testdata", self.bbmass_dir_path, filename)
        if is_csv_file(filepath):
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                _ = next(reader)  # Skips header
                for row in reader:
                    print(row)

    def save_key_column(self, filename: str):
        filepath = os.path.join(os.getcwd(), "testdata", self.bbmass_dir_path, filename)
        df = pd.read_csv(filepath)
        keys = df.key
        return keys

    def save_action_column(self, filename: str):
        filepath = os.path.join(os.getcwd(), "testdata", self.bbmass_dir_path, filename)
        df = pd.read_csv(filepath)
        actions = df.direction
        return actions

    def save_time_column(self, filename: str):
        filepath = os.path.join(os.getcwd(), "testdata", self.bbmass_dir_path, filename)
        df = pd.read_csv(filepath)
        times = df.time
        return times

    def update_action_column(self, actions: pd.core.series.Series):
        updated_actions = []
        for i in actions:
            if i == 0:
                updated_actions.append("P")
            if i == 1:
                updated_actions.append("R")
        return updated_actions

    def create_new_csv(self, keys, actions, times, filename: str):
        assert len(keys) == len(actions) == len(times)
        filepath = os.path.join(os.getcwd(), "testdata", "gen", filename)
        path = Path(filepath)
        path.touch(exist_ok=True)
        with open(path, "w+") as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            r = len(actions)
            for i in range(r):
                data = [actions[i], keys[i], times[i]]
                writer.writerow(data)

    def create_new_data(self, filename: str):
        if is_csv_file(filename):
            keys = conv.save_key_column(filename)
            times = conv.save_time_column(filename)
            actions = conv.save_action_column(filename)
            update_action_column = conv.update_action_column(actions)
            return (keys, times, update_action_column)
        else:
            raise NoCSVFileError(filename, filename + " is not a CSV file")


if __name__ == "__main__":
    check_gen_dir()
    conv = BBMASSConverter("bbmass")
    dir_path = os.path.join(os.getcwd(), "testdata", conv.get_bbmass_directory_path())
    for filename in os.listdir(dir_path):
        if is_csv_file(filename):
            # print(filename)
            filepath = os.path.join(dir_path, filename)
            # print(filepath)
            keys, update_action_column, times = conv.create_new_data(filename)
            conv.create_new_csv(keys, update_action_column, times, "gen_" + filename)
        elif is_csv_file(filename) == False:
            # Here we don't want to raise an exception because it is possible that a hidden file could stop the iteration
            # so rather than penalize the user, we can just skip it
            continue
