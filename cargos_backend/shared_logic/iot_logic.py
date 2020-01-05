IOT_URL = "http://6b2c7290.ngrok.io"

FREE_POSES = [True, True, True]


def get_free_pos():
    for idx, val in enumerate(FREE_POSES):
        if val:
            FREE_POSES[idx] = False
            return idx
    return -1


def get_occupied():
    for idx, val in enumerate(FREE_POSES):
        if not val:
            FREE_POSES[idx] = True
            return idx
    return -1
