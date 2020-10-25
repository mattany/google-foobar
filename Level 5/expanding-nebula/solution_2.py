import copy

empty = 0
gas = 1
unknown = 5


class Cell(object):
    def __init__(self, val, tl=None, tr=None, bl=None, br=None):
        assert val == 0 or val == 1 or val == unknown
        self.val = val
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br

    def __nonzero__(self):
        return self.val

    def __eq__(self, other):
        if type(other) != Cell:
            return False
        return self.val == other.val


    def is_empty(self):
        return self.tl is None and self.tr is None and self.bl is None and self.br is None

    def destroy(self):
        if self.tl is not None:
            self.tl.destroy()
        if self.tr is not None:
            self.tr.destroy()
        if self.bl is not None:
            self.bl.destroy()
        if self.br is not None:
            self.br.destroy()


class Quartet(object):
    def __init__(self, conf=None, tl=None, tr=None, bl=None, br=None):
        assert all(_ is None or type(_) is Cell for _ in (tl, tr, bl, br))
        self.conf, self.tl, self.tr, self.bl, self.br = conf, tl, tr, bl, br
        if conf is not None:
            conf.add(self)
        if self.tl is not None:
            self.tl.tl = self
        if self.tr is not None:
            self.tr.tr = self
        if self.bl is not None:
            self.bl.bl = self
        if self.br is not None:
            self.br.br = self

    def get_state(self):
        q_val = self.tl.val + self.tr.val + self.bl.val + self.br.val
        if q_val >= 5:
            if q_val % 5 > 1:
                return empty
            else:
                return unknown
        elif q_val > 1 or q_val == 0:
            return empty
        else:
            return gas

    def destroy(self):
        if self.conf != None and self in self.conf._quartets:
            self.conf.remove(self)
            self.conf = None
        if self.tl is not None:
            self.tl.tl = None
            if self.tl.is_empty():
                self.tl = None
        if self.tr is not None:
            self.tr.tr = None
            if self.tr.is_empty():
                self.tr = None
        if self.bl is not None:
            self.bl.bl = None
            if self.bl.is_empty():
                self.bl = None
        if self.br is not None:
            self.br.br = None
            if self.br.is_empty():
                self.br = None

        if self.tl is not None:
            self.tl.destroy()
            self.tl = None
        if self.tr is not None:
            self.tr.destroy()
            self.tr = None
        if self.bl is not None:
            self.bl.destroy()
            self.bl = None
        if self.br is not None:
            self.br.destroy()
            self.br = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return self.tl == other.tl and self.tr == other.tr and self.bl == other.bl and self.br == other.br

    def __repr__(self):
        # val = self.tl.val * 8 + self.tr.val * 4 + self.bl.val * 2 + self.br.val
        return (self.tl.val, self.tr.val, self.bl.val, self.br.val).__repr__()


class Configuration(object):
    def __init__(self):
        self._quartets = set()
        self.size = 0

    def add(self, quartet):
        if all(_ != quartet for _ in self._quartets):
            self._quartets.add(quartet)
            self.size += 1
            quartet.conf = self

    def remove(self, quartet):
        self._quartets.remove(quartet)
        self.size = len(self._quartets)


    def __repr__(self):
        return self._quartets.__repr__()

    def __iter__(self):
        return self._quartets.__iter__()


def create_configurations(input_matrix):
    mat_length, row_length = len(input_matrix), len(input_matrix[0])
    to_remove, to_add = set(), set()
    output_matrix = [[Configuration() for _ in xrange(row_length)] for _ in xrange(mat_length)]
    for i in xrange(mat_length):
        for j in xrange(row_length):
            conf = output_matrix[i][j]
            if i == 0:
                if j == 0:
                    case_top_left(conf, i, input_matrix, j)
                else:
                    case_top(conf, i, input_matrix, j, to_add, to_remove)
            else:
                if j == 0:
                    case_left(conf, i, input_matrix, j, to_add, to_remove)
                else:
                    case_other(conf, i, input_matrix, j, to_add, to_remove)
            for _ in to_add:
                conf.add(_)
            for _ in to_remove:
                # TODO
                for row in output_matrix:
                    print row
                print
                _.destroy()

            for q in conf:
                if i < row_length - 1:
                    Quartet(output_matrix[i + 1][j], tl=q.bl, tr=q.br, bl=Cell(unknown), br=Cell(unknown))
                if i == 0 and j < row_length - 1:
                    Quartet(output_matrix[i][j + 1], tl=q.tr, tr=Cell(unknown), bl=q.br, br=Cell(unknown))
                elif i > 0 and j < row_length - 1:
                    for qq in output_matrix[i][j + 1]:
                        qq.bl.val = q.br.val
    return output_matrix


def case_other(conf, i, input_matrix, j, to_add, to_remove):
    if input_matrix[i][j] == gas:
        for q in conf:
            if q.get_state() == empty:
                to_remove.add(q)
            else:
                assert q.get_state() == unknown
                cells = [q.tl, q.tr, q.bl, q.br]
                total_value = sum(_.val for _ in cells)
                if total_value % 5 == 1:

                    assert q.tl.val + q.tr.val + q.bl.val == 1
                    q.br.val = 0
                else:
                    assert q.tl.val == 0 and q.tr.val == 0 and q.bl.val == 0 and q.br.val == 5
                    q.br.val = 1
    else:
        for q in conf:
            cells = [q.tl, q.tr, q.bl, q.br]
            total_value = sum(_.val for _ in cells)
            if total_value % 5 == 1:
                assert q.tl.val + q.tr.val + q.bl.val == 1 and q.br.val == 5
                q.br.val = 1
            elif total_value % 5 > 1:
                q.br.val = 1
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=q.bl, br=Cell(0)))
            else:
                q.br.val = 0


def case_left(conf, i, input_matrix, j, to_add, to_remove):
    if input_matrix[i][j] == gas:
        for q in conf:
            if q.get_state() == empty:
                to_remove.add(q)
            else:
                assert q.get_state() == unknown
                cells = [q.tl, q.tr, q.bl, q.br]
                total_value = sum(_.val for _ in cells)
                if total_value % 5 == 1:
                    assert q.tl.val + q.tr.val == 1
                    q.tr.val, q.br.val = 0, 0
                else:
                    assert q.tl.val == 0 and q.tr.val == 0 and q.bl.val == 5 and q.br.val == 5
                    q.bl.val, q.br.val = 1, 0
                    to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(0), br=Cell(1)))
    else:
        for q in conf:
            assert q.get_state() == unknown
            cells = [q.tl, q.tr, q.bl, q.br]
            total_value = sum(_.val for _ in cells)
            if total_value % 5 == 1:
                assert q.tl.val + q.tr.val == 1 and q.bl.val == 5 and q.br.val == 5
                q.bl.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(0), br=Cell(1)))
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(1), br=Cell(0)))
            elif total_value % 5 == 2:
                assert q.tl.val == 1 and q.tr.val == 1 and q.bl.val == 5 and q.br.val == 5
                q.bl.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(0), br=Cell(1)))
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(1), br=Cell(0)))
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(0), br=Cell(0)))
            else:
                assert q.tl.val == 0 and q.tr.val == 0 and q.bl.val == 5 and q.br.val == 5
                q.bl.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(0), br=Cell(0)))



def case_top(conf, i, input_matrix, j, to_add, to_remove):
    if input_matrix[i][j] == gas:
        for q in conf:
            if q.get_state() == empty:
                to_remove.add(q)
            else:
                assert q.get_state() == unknown
                cells = [q.tl, q.tr, q.bl, q.br]
                total_value = sum(_.val for _ in cells)
                if total_value % 5 == 1:
                    assert q.tl.val + q.bl.val == 1
                    q.tr.val, q.br.val = 0, 0
                else:
                    assert q.tl.val == 0 and q.bl.val == 0 and q.tr.val == 5 and q.br.val == 5
                    q.tr.val, q.br.val = 1, 0
                    to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=Cell(1)))
    else:
        for q in conf:
            assert q.get_state() == unknown
            cells = [q.tl, q.tr, q.bl, q.br]
            total_value = sum(_.val for _ in cells)
            if total_value % 5 == 1:
                assert q.tl.val + q.bl.val == 1 and q.tr.val == 5 and q.br.val == 5
                q.tr.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=Cell(1)))
                to_add.add(Quartet(tl=q.tl, tr=Cell(1), bl=q.bl, br=Cell(0)))
            elif total_value % 5 == 2:
                assert q.tl.val == 1 and q.bl.val == 1 and q.tr.val == 5 and q.br.val == 5
                q.tr.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=Cell(1)))
                to_add.add(Quartet(tl=q.tl, tr=Cell(1), bl=q.bl, br=Cell(0)))
                to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=Cell(0)))
            else:
                assert q.tl.val == 0 and q.bl.val == 0 and q.tr.val == 5 and q.br.val == 5
                q.tr.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=Cell(0)))


def case_top_left(conf, i, input_matrix, j):
    if input_matrix[i][j] == gas:
        Quartet(conf, Cell(0), Cell(0), Cell(0), Cell(1))
        Quartet(conf, Cell(0), Cell(0), Cell(1), Cell(0))
        Quartet(conf, Cell(0), Cell(1), Cell(0), Cell(0))
        Quartet(conf, Cell(1), Cell(0), Cell(0), Cell(0))
    else:
        Quartet(conf, Cell(0), Cell(0), Cell(0), Cell(0))
        Quartet(conf, Cell(0), Cell(0), Cell(1), Cell(1))
        Quartet(conf, Cell(0), Cell(1), Cell(0), Cell(1))
        Quartet(conf, Cell(0), Cell(1), Cell(1), Cell(0))
        Quartet(conf, Cell(0), Cell(1), Cell(1), Cell(1))
        Quartet(conf, Cell(1), Cell(0), Cell(0), Cell(1))
        Quartet(conf, Cell(1), Cell(0), Cell(1), Cell(0))
        Quartet(conf, Cell(1), Cell(0), Cell(1), Cell(1))
        Quartet(conf, Cell(1), Cell(1), Cell(0), Cell(0))
        Quartet(conf, Cell(1), Cell(1), Cell(0), Cell(1))
        Quartet(conf, Cell(1), Cell(1), Cell(1), Cell(0))
        Quartet(conf, Cell(1), Cell(1), Cell(1), Cell(1))


input_0 = [[True, True, False, True, False, True, False, True, True, False],
           [True, True, False, False, False, False, True, True, True, False],
           [True, True, False, False, False, False, False, False, False, True],
           [False, True, False, False, False, False, True, True, False, False]]

input_1 = [[True, False, True], [False, True, False], [True, False, True]]

input_2 = [[True, False, True, False, False, True, True, True],
           [True, False, True, False, False, False, True, False],
           [True, True, True, False, False, False, True, False],
           [True, False, True, False, False, False, True, False],
           [True, False, True, False, False, True, True, True]]
create_configurations(input_1)
