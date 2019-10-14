class Volume(object):
    def __init__(self, height, length, width):
        self.height = height
        self.length = length
        self.width = width

    def volume(self):
        return self.height * self.width * self.length


class Cell(Volume):
    def __init__(self, height, length, width, is_free):
        super().__init__(height, length, width)
        self.is_free = is_free


class Cargo(Volume):
    def __init__(self, height, length, width, rotatable):
        super().__init__(height, length, width)
        self.rotatable = rotatable
