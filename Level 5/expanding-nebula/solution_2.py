import copy

empty = 0
gas = 1
unknown = 5


class Cell(object):
    def __init__(self, val):
        assert val == 0 or val == 1 or val == unknown
        self.val = val
        self.destroyed = False
        self.tl = set()
        self.tr = set()
        self.bl = set()
        self.br = set()

    def __nonzero__(self):
        return self.val

    def __eq__(self, other):
        if type(other) != Cell:
            return False
        return self.val == other.val

    def is_empty(self):
        return self.tl is None and self.tr is None and self.bl is None and self.br is None

    def destroy(self):
        if not self.destroyed:
            self.destroyed = True
            temp = self.tl | self.tr | self.bl | self.br
            for _ in temp:
                _.destroy()


class Quartet(object):
    def __init__(self, conf=None, tl=None, tr=None, bl=None, br=None):
        assert all(_ is None or type(_) is Cell for _ in (tl, tr, bl, br))
        self.destroyed = False
        self.conf, self.tl, self.tr, self.bl, self.br = conf, tl, tr, bl, br
        if conf is not None:
            self.add_to_conf(conf)
        if self.tl is not None:
            self.tl.tl.add(self)
        if self.tr is not None:
            self.tr.tr.add(self)
        if self.bl is not None:
            self.bl.bl.add(self)
        if self.br is not None:
            self.br.br.add(self)

    def set_tl(self, cell):
        assert self.tl.val == 5
        self.tl = cell
        self.tl.tl.add(self)

    def set_tr(self, cell):
        assert self.tr.val == 5
        self.tr = cell
        self.tr.tr.add(self)

    def set_bl(self, cell):
        assert self.bl.val == 5
        self.bl = cell
        self.bl.bl.add(self)

    def set_br(self, cell):
        assert self.tl.val == 5
        self.br = cell
        self.br.br.add(self)

    def add_to_conf(self, conf):
        if not all(_ != self for _ in conf._quartets):
            self.tl, self.tr, self.bl, self.br = None, None, None, None
        else:
            conf._quartets.add(self)
            conf.size += 1
            self.conf = conf

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
        if not self.destroyed:
            self.destroyed = True
            if self.conf is not None:
                self.conf.remove(self)
                self.conf = None
            if self.tl is not None:
                self.tl.tl.remove(self)
            if self.tr is not None:
                self.tr.tr.remove(self)
            if self.bl is not None:
                self.bl.bl.remove(self)
            if self.br is not None:
                self.br.br.remove(self)

            if self.tl is not None:
                if not self.tl.tl:
                    self.tl.destroy()
            if self.tr is not None:
                if not self.tr.tr:
                    self.tr.destroy()
            if self.bl is not None:
                if not self.bl.bl:
                    self.bl.destroy()
            if self.br is not None:
                if not self.br.br:
                    self.br.destroy()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return self.tl == other.tl and self.tr == other.tr and self.bl == other.bl and self.br == other.br

    def __repr__(self):
        # val = self.tl.val * 8 + self.tr.val * 4 + self.bl.val * 2 + self.br.val
        return (self.tl.val, self.tr.val, self.bl.val, self.br.val).__repr__()
        # return self.tl.val.__repr__()


class Configuration(object):
    def __init__(self, i, j):
        self._quartets = set()
        self.size = 0
        self.location = (i, j)

    # def add(self, quartet):
    #     if all(_ != quartet for _ in self._quartets):
    #         self._quartets.add(quartet)
    #         self.size += 1
    #         quartet.conf = self
    #         return True
    #     else:
    #         quartet.destroy()
    #     return False
    def remove(self, quartet):
        self._quartets.remove(quartet)
        self.size = len(self._quartets)

    def __repr__(self):
        return self._quartets.__repr__()

    def __iter__(self):
        return self._quartets.__iter__()


def create_configurations(input_matrix):
    global qid
    qid = 0
    mat_length, row_length = len(input_matrix), len(input_matrix[0])
    output_matrix = [[Configuration(i, j) for j in xrange(row_length)] for i in xrange(mat_length)]
    for i in xrange(mat_length):
        for j in xrange(row_length):
            print i, j
            for row in output_matrix:
                for _ in row:
                    print _
            print
            to_remove, to_add = set(), set()
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
            # print "conf location: ", conf.location
            # print "size before add: ", conf.size
            # print "to add: ", to_add
            for _ in to_add:
                _.add_to_conf(conf)
            # for row in output_matrix:
            # for _ in row:
            # print row
            # print
            # print "size after add: ", conf.size
            # print "to remove: ", len(to_remove)
            for _ in to_remove:
                _.destroy()
            # print "size after remove: ", conf.size
            # print
            # new_conf = Configuration(i, j)
            to_add, to_remove = set(), set()
            for q in conf:
                if i < row_length - 1:
                    Quartet(output_matrix[i + 1][j], tl=q.bl, tr=q.br, bl=Cell(unknown), br=Cell(unknown))
                if i == 0 and j < row_length - 1:
                    Quartet(output_matrix[i][j + 1], tl=q.tr, tr=Cell(unknown), bl=q.br, br=Cell(unknown))
                elif i > 0 and j < row_length - 1:
                    to_remove |=  {_ for _ in output_matrix[i][j + 1]}
                    for qq in output_matrix[i][j + 1]:
                        if q.tr == qq.tl:
                            if qq.bl.val == unknown:
                                to_remove.remove(qq)
                                qq.set_bl(q.br)
                            else:
                                to_add.add(Quartet(tl=qq.tl, tr=qq.tr, bl=q.br, br=Cell(unknown)))
            for _ in to_add:
                _.add_to_conf(output_matrix[i][j + 1])
            for _ in to_remove:
                _.destroy()
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
                bl1, br1 = q.bl, q.br
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=Cell(0), br=br1))
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=bl1, br=Cell(0)))
            elif total_value % 5 == 2:
                assert q.tl.val == 1 and q.tr.val == 1 and q.bl.val == 5 and q.br.val == 5
                q.bl.val, q.br.val = 1, 1
                bl0, bl1, br0, br1 = Cell(0), q.bl, Cell(0), q.br
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=bl0, br=br1))
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=bl1, br=br0))
                to_add.add(Quartet(tl=q.tl, tr=q.tr, bl=bl0, br=br0))
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
                tr1, br1 = q.tr, q.br
                to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=br1))
                to_add.add(Quartet(tl=q.tl, tr=tr1, bl=q.bl, br=Cell(0)))
            elif total_value % 5 == 2:
                assert q.tl.val == 1 and q.bl.val == 1 and q.tr.val == 5 and q.br.val == 5
                q.tr.val, q.br.val = 1, 1
                tr0, tr1, br0, br1 = Cell(0), q.tr, Cell(0), q.br
                to_add.add(Quartet(tl=q.tl, tr=tr0, bl=q.bl, br=br1))
                to_add.add(Quartet(tl=q.tl, tr=tr1, bl=q.bl, br=br0))
                to_add.add(Quartet(tl=q.tl, tr=tr0, bl=q.bl, br=br0))
            else:
                assert q.tl.val == 0 and q.bl.val == 0 and q.tr.val == 5 and q.br.val == 5
                q.tr.val, q.br.val = 1, 1
                to_add.add(Quartet(tl=q.tl, tr=Cell(0), bl=q.bl, br=Cell(0)))


def case_top_left(conf, i, input_matrix, j):
    tl0, tl1, tr0, tr1, bl0, bl1, br0, br1 = Cell(0), Cell(1), Cell(0), Cell(1), Cell(0), Cell(1), Cell(0), Cell(1)
    if input_matrix[i][j] == gas:
        Quartet(conf, tl0, tr0, bl0, br1)
        Quartet(conf, tl0, tr0, bl1, br0)
        Quartet(conf, tl0, tr1, bl0, br0)
        Quartet(conf, tl1, tr0, bl0, br0)
    else:
        Quartet(conf, tl0, tr0, bl0, br0)
        Quartet(conf, tl0, tr0, bl1, br1)
        Quartet(conf, tl0, tr1, bl0, br1)
        Quartet(conf, tl0, tr1, bl1, br0)
        Quartet(conf, tl0, tr1, bl1, br1)
        Quartet(conf, tl1, tr0, bl0, br1)
        Quartet(conf, tl1, tr0, bl1, br0)
        Quartet(conf, tl1, tr0, bl1, br1)
        Quartet(conf, tl1, tr1, bl0, br0)
        Quartet(conf, tl1, tr1, bl0, br1)
        Quartet(conf, tl1, tr1, bl1, br0)
        Quartet(conf, tl1, tr1, bl1, br1)


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
for row in create_configurations(input_1):
    for _ in row:
        print _
    print
