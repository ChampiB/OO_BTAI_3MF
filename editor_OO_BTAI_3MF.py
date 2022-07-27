from editor.Editor import Editor


def main():
    """
    Display a graphical user interface to analyse the behaviour of BTAI_3MF.
    :return: nothing.
    """
    # Create the GUI for analysis.
    gui = Editor()
    gui.loop()


if __name__ == '__main__':
    main()
