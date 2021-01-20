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
            requests.post('http://2f9f839aebbd.ngrok.io/action',
                          json.dumps(
                              {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                               'login': gui_classes.login_or_mail,
                               'action': 'offline'}))
            break
        if gui_classes.info[3] is None or scores > gui_classes.info[3]:
            requests.post('http://2f9f839aebbd.ngrok.io/change',
                          json.dumps(
                              {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                               'login': gui_classes.login_or_mail,
                               'change_this': 'score', 'change_to_this': scores}))
            requests.post('http://2f9f839aebbd.ngrok.io/change',
                          json.dumps(
                              {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                               'login': gui_classes.login_or_mail,
                               'change_this': 'last_score', 'change_to_this': scores}))
        else:
            requests.post('http://2f9f839aebbd.ngrok.io/change',
                          json.dumps(
                              {'version': 1.0, 'ip': socket.gethostbyname(socket.gethostname()),
                               'login': gui_classes.login_or_mail,
                               'change_this': 'last_score', 'change_to_this': scores}))
        bool_ = gui_classes.open_main_window()
