def logout():
    exit_check(True)


def exit_check(exit):
    if exit:
        raise Exception('Exiting')

