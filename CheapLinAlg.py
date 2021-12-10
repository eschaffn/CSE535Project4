import torch

gpu = False


class CheapVector:
    def __init__(self):
        self.index = {}
        self.zero_val = 0

    # returns value of e^th coordinate of self
    def get_entry(self, e):
        if e in self.index.keys():
            return self.index[e]

        return self.zero_val

    # updates value of e^th coordinate of self
    def update_entry(self, e, val):
        if val == self.zero_val:
            if e in self.index.keys():
                self.index.pop(e)
        else:
            self.index.update({e: val})

    # returns json-serializable representation of self
    def to_json(self):
        out = {
            'zero_val': self.zero_val,
            'index': self.index
        }

        return out

    # re-creates row vector from dictionary loaded from json file
    def from_json(self, f):
        self.zero_val = f['zero_val']

        for k in f['index'].keys():
            self.index.update({int(k): f['index'][k]})


class CheapSquareMatrix:
    def __init__(self, elems=None):
        self.elems = elems
        self.row_index = {}
        self.zero_val = 0

    # change value of <x, y>^th entry of self (x = row, y = column)
    def update_entry(self, x, y, val):
        if x in self.row_index.keys():
            self.row_index[x].update_entry(y, val)
        elif not val == self.zero_val:
            new_vec = CheapVector()
            new_vec.zero_val = self.zero_val
            new_vec.update_entry(y, val)
            self.row_index.update({x: new_vec})

    # outputs value of <x, y>^th entry of self
    def get_entry(self, x, y):
        if x in self.row_index.keys():
            return self.row_index[x].get_entry(y)

        return self.zero_val

    # outputs result of multiplying vector v with self:
    # right=True ==> (self)*(v),  right=False ==> (v)*(self)
    def as_linear_map(self, v, right=True):
        get_vec = self.get_row_vec if right else self.get_col_vec
        vec = torch.tensor([torch.vdot(v, get_vec(self.elems[i])).item() for i in range(len(self.elems))], dtype=torch.float32)

        if gpu:
            vec.cuda()

        return vec

    # returns e^th row vector
    def get_row_vec(self, e):
        vec = torch.tensor([self.get_entry(e, self.elems[i]) for i in range(len(self.elems))], dtype=torch.float32)

        if gpu:
            vec.cuda()

        return vec

    # returns e^th column vector
    def get_col_vec(self, e):
        vec = torch.tensor([self.get_entry(self.elems[i], e) for i in range(len(self.elems))], dtype=torch.float32)

        if gpu:
            vec.cuda()

        return vec

    # returns json-serializable representation of self
    def to_json(self):
        out = {
            'zero_val': self.zero_val,
            'elems': self.elems,
            'index': [(x, self.row_index[x].to_json()) for x in self.row_index.keys()]
        }

        return out

    # re-creates matrix from dictionary loaded from json file
    def from_json(self, f):
        self.zero_val = f['zero_val']
        self.elems = f['elems']

        for x in f['index']:
            new_vec = CheapVector()
            new_vec.from_json(x[1])
            self.row_index.update({int(x[0]): new_vec})


# re-creates state vector from json file
def vec_from_json(vlist):
    vec = torch.tensor(vlist, dtype=torch.float32)

    if gpu:
        vec.cuda()

    return vec
