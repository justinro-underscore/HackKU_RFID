from tools import get_token, get_registrant, set_registrant_rfid
from datetime import datetime

def check_confirmation(question_str):
    in_str = input("{} (Y/n) ".format(question_str)).lower()
    if in_str == "" or in_str == "y" or in_str == "yes":
        return True
    return False

def run_registration():
    print("Welcome to HackKU RFID registration!")
    print("Retrieving token...")
    try:
        token = get_token()
        print("Token received!")
    except:
        print("Error: Token could not be retrieved")
        print("Please try again.")
        exit()

    while True:
        print("-~" * 20)
        email = input("Enter email: ")
        if email == "exit":
            return
        try:
            reg = get_registrant(email, token)
            if check_confirmation("Is {} {} ({}) correct?".format(reg["first_name"], reg["last_name"], reg["email"])):
                if reg["rfid"]:
                    if not check_confirmation("Warning! Person already has RFID set for them, do you want to override?"):
                        print("Registration cancelled")
                        continue
                if reg["level_of_study"] == "High School":
                    print("\nNOTE: This person is in high school. Verify and give them a Minor Participant form\n")
                if datetime.strptime(reg["date"], "%a, %d %b %Y %H:%M:%S %Z").date() == datetime.now().date():
                    print("\nNOTE: This person has registered today. Do not give them a swag bag!\n")
                rfid = input("Scan RFID card: ")
                print("Registering {} for {}".format(rfid, reg["first_name"] + " " + reg["last_name"]))
                set_registrant_rfid(email, token, rfid)
            else:
                print("Registration cancelled")
        except RuntimeError as e:
            print(e)

run_registration()