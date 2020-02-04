# HackKU RFID

This is the RFID system that is used for HackKU 2020

## How to Set Up

Make sure you have python3 installed, then run the following commands:

```bash
sudo apt-get install python3-tk
pip3 install -r requirements.txt
```

After that, you should be setup and ready to go! If anything goes wrong, consult [this tutorial](https://pimylifeup.com/raspberry-pi-rfid-rc522/)

## `local_data`

The `local_data` folder is referenced extensively, and will not work if you do not have it on your local machine. This contains knowledge that should not be released on the web, hence it is in the .gitignore. So this is how it should be set up:

```
local_data
├── api_key.txt             # Defines what URL the API is using
├── credentials.json        # Credentials used with Google Sheets
├── google_sheets_id.txt    # Defines the ID used to pull the Google Sheets schedule
├── private_key.txt         # Defines the private key used to interface with the HackKU information
├── token.pickle            # Stores credential information for Google Sheets
```
