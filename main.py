import json
import socket

import requests

import gui_classes

if __name__ == '__main__':
    bool_ = gui_classes.main()
    while bool_:
        exec(open('game_classes.py', 'r').read())
        with open('scores.txt', 'r') as file:
            scores = file.read()
        if scores == 'None':
            break
        bool_ = gui_classes.open_main_window()
    requests.post('https://b2a076121e8e.ngrok.io/action',
                  json.dumps(
                      {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                       'login': gui_classes.login_or_mail,
                       'action': 'offline'}))
