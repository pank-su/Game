from gui_classes import main




if __name__ == '__main__':
    bool_ = main()
    if bool_:
        while True:
            exec(open('game_classes.py', 'r').read())
            break

