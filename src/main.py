from src.automate import automate
from src.file import file_transfer
import yaml
import os

file = os.path.abspath("../config.yaml")
stream = open(file, 'r')
configuration = yaml.load(stream)

server = configuration['RASPBERRY_PI']['IP']
port = configuration['RASPBERRY_PI']['PORT']
file = os.path.abspath("../transfer_data/data.csv")
user = configuration['RASPBERRY_PI']['USER']
password = str(configuration['RASPBERRY_PI']['PASSWORD'])

if __name__ == "__main__":
    temp = True
    file_transfer = file_transfer.Transfer(server=server,
                                           port=port,
                                           file_path=file,
                                           user=user,
                                           password=password)

    automation = automate.Automation(file_transfer=file_transfer)

    print("Select the following operation:")
    while temp:
        print("1: Record Automation\n"
              "2: Run Automation Loop\n"
              "3: Transfer Test File (Debug Tool)\n"
              "4: Exit\n\n")
        user_input = int(input())
        if user_input == 1:
            automation.create_automation()
        elif user_input == 2:
            automation.automate()
        elif user_input == 3:
            file_transfer.scp_put()
        elif user_input == 4:
            exit(0)
        else:
            print("Invalid choice. Please choose again")
