# TODO LEARN OOP

# class Volume(object):
#     def __init__(self, height, length, width):
#         self.height = height
#         self.length = length
#         self.width = width
#
#     def volume(self):
#         return self.height * self.width * self.length
#
#     def __str__(self):
#         return str(self.height) + ' ' + str(self.length) + ' ' + str(self.width)


class Cell(object):
    def __init__(self, height, length, width):
        self.height = height
        self.length = length
        self.width = width

    def volume(self):
        return self.height * self.width * self.length

    def __str__(self):
        return str(self.height) + ' ' + str(self.length) + ' ' + str(self.width)


class Cargo(object):
    def __init__(self, height, length, width, rotatable):
        self.height = height
        self.length = length
        self.width = width
        self.rotatable = rotatable

    def volume(self):
        return self.height * self.width * self.length

    def __str__(self):
        return str(self.height) + ' ' + str(self.length) + ' ' + str(self.width)
