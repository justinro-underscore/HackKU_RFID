from tools import get_token, get_registrant, set_registrant_rfid

def check_confirmation(obj_str):
    in_str = input("Is {} correct? (Y/n) ".format(obj_str)).lower()
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
            if check_confirmation("{} {} ({})".format(reg["first_name"], reg["last_name"], reg["rfid"])):
                rfid = input("Scan RFID card: ")
                print("Registering {} for {}".format(rfid, reg["first_name"] + " " + reg["last_name"]))
                set_registrant_rfid(email, token, rfid)
            else:
                print("Registration cancelled")
        except RuntimeError as e:
            print(e)

run_registration()