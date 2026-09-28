class rimb:
    def __init__(self, storona_a, kut_a):
        self.storona_a = storona_a
        self.kut_a = kut_a

    def __setattr__(self, name, value):
        if name == "storona_a":
            if value <= 0:
                return None

        if name == "kut_a":
            if value <= 0 or value >= 180:
                return None
            object.__setattr__(self, "kut_a", value)
            object.__setattr__(self, "kut_b", 180-value)
            return
        object.__setattr__(self, name, value)

    def  __repr__(self):
        return f'{self.storona_a}, {self.kut_a}, {self.kut_b}'
romb = rimb(4, 30)
print(romb)