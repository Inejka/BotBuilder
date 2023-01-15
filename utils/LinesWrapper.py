class Point:
    def __init__(self, update_callback, x, y):
        self.container = [x, y]
        self.update_callback = update_callback
        self.transit_parent_id = None

    def set_transit_parent_id(self, transit_parent_id):
        self.transit_parent_id = transit_parent_id

    def get_transit_parent_id(self):
        return self.transit_parent_id

    def __next__(self):
        return self.container.__next__()

    def __iter__(self):
        return self.container.__iter__()

    def __getitem__(self, item):
        return self.container.__getitem__(item)

    def __setitem__(self, key, value):
        self.update_callback()
        self.container[key] = value


class Line:
    def __init__(self, update_callback, from_id, x1=0, y1=0, x2=0, y2=0):
        self.container = [Point(update_callback, x1, y1), Point(update_callback, x2, y2)]
        self.update_callback = update_callback
        self.from_id = from_id
        self.transit_id = None

    def set_transit_id(self, transit_id):
        self.transit_id = transit_id
        self.container[0].set_transit_parent_id(transit_id)
        self.container[1].set_transit_parent_id(transit_id)

    def get_transit_id(self):
        return self.transit_id

    def __next__(self):
        return self.container.__next__()

    def __iter__(self):
        return self.container.__iter__()

    def __getitem__(self, item):
        return self.container.__getitem__(item)

    def __setitem__(self, key, value):
        self.container[key] = value


class LinesWrapper:
    def __init__(self, update_callback):
        self.lines = []
        self.update_callback = update_callback

    def __next__(self):
        return self.lines.__next__()

    def __iter__(self):
        return self.lines.__iter__()

    def add_line(self, line):
        self.lines.append(line)
        self.update_callback()

    def remove_line(self, line):
        self.lines.remove(line)
        self.update_callback()
