class CheapVector:
    def __init__(self, elems):
        self.zero_val = 0
        self.elems = elems
        self.index = {}

    # change value of e^th coordinate
    def update_entry(self, e, val):
        if not val == self.zero_val:
            self.index.update({e: val - self.zero_val})

    # get value of e^th coordinate
    def get_entry(self, e):
        if e in self.index.keys():
            return self.index[e] + self.zero_val

        return self.zero_val

    # outputs result of adding vector v to self
    def add(self, v):
        out = CheapVector(self.elems)
        used = set()

        for x in v.index.keys():
            val = 0

            if x in self.index.keys():
                val = self.index[x]
                used.add(x)

            out.index.update({x: val + v.index[x]})

        for x in [e for e in self.index.keys() if e not in used]:
            out.index.update({x: self.index[x]})

        out.zero_val = self.zero_val + v.zero_val

        return out

    # scalar multiplication (no output-- just changes self)
    def scalar_mul(self, scalar):
        self.zero_val *= scalar

        for x in self.index.keys():
            self.index[x] *= scalar

    # add n to each entry of self
    def add_uniform_vec(self, n):
        self.zero_val += n

    # don't worry about this one lol
    def update(self):
        for x in self.index.keys():
            if self.index[x] == 0:
                self.index.pop(x)

    # outputs vector as list
    def tolist(self):
        out = []

        for e in self.elems:
            out.append(self.get_entry(e))

        return out


class CheapSquareMatrix:
    def __init__(self, elems):
        self.zero_val = 0
        self.elems = elems
        self.row_index = {}

    # outputs transpose of self
    def transpose(self):
        out = CheapSquareMatrix(self.elems)
        out.zero_val = self.zero_val

        for x in self.row_index.keys():
            for y in self.row_index[x].keys():
                if y in out.row_index.keys():
                    out.row_index[y].update({x: self.row_index[x][y]})
                else:
                    out.row_index.update({y: {x: self.row_index[x][y]}})

        return out

    # change value of <x, y>^th entry of self (x = row, y = column)
    def update_entry(self, x, y, val):
        if not val == self.zero_val:
            if x in self.row_index.keys():
                self.row_index[x].update({y: val - self.zero_val})
            else:
                self.row_index.update({x: {y: val - self.zero_val}})

    # outputs value of <x, y>^th entry of self
    def get_entry(self, x, y):
        if x in self.row_index.keys():
            if y in self.row_index[x].keys():
                return self.row_index[x][y] + self.zero_val

        return self.zero_val

    # adds n to each entry of self
    def add_matrix_of_ns(self, n):
        self.zero_val += n

    # outputs result of adding matrix m to self
    def add(self, m):
        out = CheapSquareMatrix(self.elems)
        used = set()

        for x in m.row_index.keys():
            for y in m.row_index[x].keys():
                val = 0

                if x in self.row_index.keys() and y in self.row_index[x].keys():
                    val = self.row_index[x][y]
                    used.add((x, y))

                out.update_entry(x, y, val + m.row_index[x][y])

        for x in self.row_index.keys():
            for y in [k for k in self.row_index[x].keys() if (x, k) not in used]:
                out.update_entry(x, y, self.row_index[x][y])

        out.zero_val = self.zero_val + m.zero_val

        return out

    # outputs result of multiplying self by matrix m (self = left-hand, m = right-hand)
    def mul(self, m):
        out = CheapSquareMatrix(self.elems)
        m1 = m.transpose()

        for e_x in self.elems:
            for e_y in self.elems:
                val = 0
                zr = e_x not in self.row_index.keys()
                zc = e_y not in m1.row_index.keys()

                if zr and zc:
                    val = len(self.elems) * self.zero_val * m.zero_val
                elif zr:
                    for e_z in self.elems:
                        val += m1.get_entry(e_y, e_z)
                        val *= self.zero_val
                elif zc:
                    for e_z in self.elems:
                        val += self.get_entry(e_x, e_z)
                        val *= m1.zero_val
                else:
                    for e_z in self.elems:
                        val += self.get_entry(e_x, e_z) * m1.get_entry(e_y, e_z)

                out.update_entry(e_x, e_y, val)

        return out

    # scalar multiplication (no output-- just changes self)
    def scalar_mul(self, scalar):
        self.zero_val *= scalar

        for x in self.row_index.keys():
            for y in self.row_index[x].keys():
                self.row_index[x][y] *= scalar

    # don't worry about this one either lol
    def update(self):
        for x in self.row_index.keys():
            if len(list(self.row_index[x].keys())) == 0:
                self.row_index.pop(x)
            else:
                for y in self.row_index[x].keys():
                    if self.row_index[x][y] == 0:
                        self.row_index[x].pop(y)

    # outputs result of multiplying vector v with self
    # if right=true:    self*vec
    # if right=false:   vec*self
    def as_linear_map(self, v, right=True):
        if len(list(v.index.keys())) == 0 and v.zero_val == 0:
            return v

        out = CheapVector(self.elems)

        for e_x in self.elems:
            val = 0

            for e_y in self.elems:
                if right:
                    val += self.get_entry(e_x, e_y) * v.get_entry(e_y)
                else:
                    val += self.get_entry(e_y, e_x) * v.get_entry(e_y)

            out.update_entry(e_x, val)

        out.update()

        return out

    # outputs matrix as list of lists of values
    def tolist(self):
        out = []

        for j in range(len(self.elems)):
            out.append([])

            for k in range(len(self.elems)):
                out[j].append(self.get_entry(self.elems[j], self.elems[k]))

        return out


def print_matrix(matrix):
    matrix_list = matrix.tolist()

    for n in range(len(matrix_list)):
        print(matrix_list[n])


if __name__ == "__main__":
    """
    adding a number n to each coordinate of a vector/matrix doesn't use any memory-- it is saved as the "base value",
    and each coordinate only uses memory if it is different from the "base value" (it saves the difference between
    the coordinate and the "base value")
    """

    # list of coordinates (dimension) -- can be any list
    coords = [(x + 1) for x in range(3)]
    vec = CheapVector(coords)
    vec2 = CheapVector(coords)
    mat1 = CheapSquareMatrix(coords)
    mat2 = CheapSquareMatrix(coords)

    # initialize mat1 as a matrix of all 2s, then change entries (1,1),(2,2),(3,2) to 1
    mat1.add_matrix_of_ns(2)
    mat1.update_entry(1, 1, 1)
    mat1.update_entry(2, 2, 1)
    mat1.update_entry(3, 2, 1)

    print("Matrix 1:")
    print_matrix(mat1)

    mat2.update_entry(1, 1, 1)
    mat2.update_entry(1, 3, 1)
    mat2.update_entry(3, 1, 1)
    mat2.update_entry(3, 3, 1)

    print("\nMatrix 2:")
    print_matrix(mat2)

    mat = mat1.add(mat2)

    print("\nMatrix 3 = Matrix 1 + Matrix 2:")
    print_matrix(mat)

    # initialize each coord. of vec as 2s, then change 1st coord. to 3
    vec.zero_val = 2
    vec.update_entry(1, 3)

    print("\nVector 1:")
    print(vec.tolist())

    # coords of vec2 (implicitly) initialized as 0s, then change 2nd coord to 2, then add 3 to each coord.
    vec2.update_entry(2, 2)
    vec2.add_uniform_vec(3)
    print("\nVector 2:")
    print(vec2.tolist())
    print("\nVector 3 = Vector 1 + Vector 2:")
    print(str(vec2.add(vec).tolist()))
    print("\n[Matrix 3] * [Vector 3]: ")
    print(mat.as_linear_map(vec).tolist())
    print("\n[Vector 3] * [Matrix 3]: ")
    print(mat.as_linear_map(vec, right=False).tolist())
