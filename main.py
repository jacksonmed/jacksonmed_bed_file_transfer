from automate import automate
from file import file_transfer
import time
import yaml

stream = open("config.yaml", 'r')
configuration = yaml.load(stream)

server = configuration['RASPBERRY_PI']['IP']
port = configuration['RASPBERRY_PI']['PORT']
file = configuration['HOST']['SOURCE_PATH']
user = configuration['RASPBERRY_PI']['USER']
password = configuration['RASPBERRY_PI']['PASSWORD']


if __name__ == "__main__":
    temp = True
    print("Select the following operation:")
    automation = automate.automation()

    while temp:
        print("1: Record Automation\n"
              "2: Run Automation Loop\n"
              "3: Transfer Test File (Debug Tool)\n"
              "4: Exit\n\n")
        user_input = int(input())
        if user_input == 1:
            automation.create_automation(
                configuration['AUTOMATIONS']['DESTINATION_PATH'])
        elif user_input == 2:
            automation.automate(
                instruction_path=configuration['AUTOMATIONS']['DESTINATION_PATH'])
        elif user_input == 3:
            file_transfer = file_transfer.Transfer(server=server,
                                                   port=port,
                                                   file_path=file,
                                                   user=user,
                                                   password=password)
            file_transfer.scp_put()
        elif user_input == 4:
            exit(0)
        else:
            print("Invalid choice. Please choose again")

    # automation = automate.automation()
    # automation.create_automation('automations/test.csv')
    # print("Beginning Playback in 3 sec...")
    # time.sleep(3)
    # automation.automate('automations/test.csv')














