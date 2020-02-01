# How to Set Server Up

First, download `ngrok` from [this link here](https://dashboard.ngrok.com/get-started). This is how we will host our local server out to the world!

Next, move the server and start the virtual environment:

```bash
HackKU_RFID/server/ $ pyenv activate venv
(venv) HackKU_RFID/server/ $ pip3 install -r requirements.txt
(venv) HackKU_RFID/server/ $ python3 run.py
```

The server should start being hosted on your local machine. Next, open up a new tab and load up `ngrok` on port 5000 to publish it out on the world wide web!

```
(venv) HackKU_RFID/server/ $ ./ngrok http 5000
```

`ngrok` should output a url to connect to. You can now distribute this website and this will be the thing that everything runs off of!