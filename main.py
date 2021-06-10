from automate import automate
import time

if __name__ == "__main__":
    automation = automate.automation()
    automation.create_automation('automations/test.csv')
    print("Beginning Playback in 3 sec...")
    time.sleep(3)
    automation.automate('automations/test.csv')


    # mouse_pos.start_listen()



