class alias(object):
    def _init(self, string, name, bind):
        if name == None:
            name = get(string, "(", ")")
        if bind == None:
            bind = get(string, "`", "`")
        down = get(string, "'", "'")
        up = get(string, '"', '"')
        return name, bind, up, down

    def __init__(self, string, name=None, bind=None):
        name, bind, up, down = self._init(string, name, bind)
        self.names = [name]
        self.name = name
        self.bind = bind
        self.down = [down] if down != None else []
        self.up = [up] if up != None else []

    def add(self, string, name, bind, b, n):
        name, bind, up, down = self._init(string, name, bind)
        if not b:
            if self.bind == None:
                self.bind = bind
            elif bind != None:
                print "WRONG BINDS,", bind, self.bind
                print self.names
                print self.name
                return -1
        if not n:
            if self.name == None:
                self.name = name
                self.names = [name]
            elif name != None:
                self.name += name.capitalize()
                self.names.append(name)
        if down != None:
            self.down.append(down)
        if up != None:
            self.up.append(up)

    def __str__(self):
        if self.name == None:
            if self.up or len(self.down) > 1:
                name = self.bind.capitalize() + "_Key"
                return 'alias "+{0}" "{1}"\n{2}bind "{3}" "+{0}"'.format(
                    name,
                    ";".join(self.down),
                    'alias "-{}" "{}"\n'.format(name, ";".join(self.up)),
                    self.bind,
                )
            else:
                return 'bind "{}" "{}"'.format(self.bind, ";".join(self.down))
        if self.up or len(self.down) > 1:
            return 'alias "+{0}" "{1}"\n{4}alias "{2}" "{3}+{0}"'.format(
                self.name.upper(),
                ";".join(self.down),
                self.name,
                ""
                if self.bind == None or len(self.bind) == 0
                else "bind {} ".format(self.bind),
                'alias "-{0}" "{1}"\n'.format(self.name.upper(), ";".join(self.up))
                if self.up
                else "",
            )
        else:
            return 'alias "{}" "{}{}"'.format(
                self.name,
                ""
                if self.bind == None or len(self.bind) == 0
                else "bind {} ".format(self.bind),
                ";".join(self.down),
            )


class modifyer(object):
    def __init__(self, string, bind=None, name=None):
        if name == None:
            self.name = get(string, "(", ")")
        else:
            self.name = name
        if bind == None:
            self.bind = get(string, "|", "|")
        else:
            self.bind = bind
        self.d = True
        self.mod = get(string, "[", "]")
        if self.mod == None:
            self.mod = get(string, "{", "}")
            if self.mod != None:
                self.d = False
        down = get(string, "'", "'")
        up = get(string, '"', '"')
        self.pred = []
        self.preu = []
        self.down = []
        self.up = []
        self.sDown = [] if down == None else [down]
        self.sUp = [] if up == None else [up]
        self.nDown = []
        self.nUp = []

    def add(self, string, downInput):
        name = get(string, "(", ")")
        bind = get(string, "`", "`")
        b = [None]

        def bb():
            for i in self.down + self.up:
                b[0] = i
                yield i.bind
            n[0] = None

        n = [None]

        def nn():
            for i in self.down + self.up:
                n[0] = i
                for j in i.names:
                    yield j
            n[0] = None

        bi = False if bind == None else bind in bb()
        na = False if name == None else name in nn()
        if bi or na:
            b = b[0]
            n = n[0]
            if bi and na:
                if b != n:
                    raise "Not the same. D:"
            else:
                if b == None:
                    b = n
            b.add(string, name, bind, bi, na)
        else:
            a = alias(string, name, bind)
            (self.down if downInput else self.up).append(a)

    def _form(self):
        return "{}{}\n".format(
            "\n".join(str(i) for i in self.down), "\n".join(str(i) for i in self.up)
        )

    def _mid(self):
        return "{}\n{}\n".format(
            'alias "+{}" "{}"'.format(
                self.name.upper(),
                ";".join(i.name for i in (self.down + self.mod.up + self.pred)),
            ),
            'alias "-{}" "{}"'.format(
                self.name.upper(),
                ";".join(i.name for i in (self.up + self.mod.down + self.preu)),
            ),
        )

    def _lat(self):
        down = self.sDown + self.mod.sUp
        nDown = self.nDown
        up = self.sUp + self.nUp
        if down:
            name = self.name.capitalize() + "_Bonus"
            if self.mod.name == "":
                return 'alias "+{0}" "{1}"\nalias "-{0}" "{2}"\nbind "{3}" "+{0}"'.format(
                    name,
                    ";".join(down + ["+" + self.name.upper()] + nDown),
                    ";".join(up),
                    self.bind,
                )
            else:
                return 'alias "+{0}" "{1}"\nalias "-{0}" "{2}"\nalias "{3}" "bind {4} +{0}"'.format(
                    name,
                    ";".join(down + ["+" + self.name.upper()] + nDown),
                    ";".join(up),
                    self.name,
                    self.bind,
                )
        else:
            if self.mod.name == "":
                return 'bind "{}" "+{}"'.format(self.bind, self.name.upper())
            else:
                return 'alias "{}" "bind {} +{}"'.format(
                    self.name, self.bind, self.name.upper()
                )

    def __str__(self):
        if self.name == "":
            return self._form()
        else:
            return "{}{}{}\n".format(self._form(), self._mid(), self._lat())

    def call(self):
        if len(self.name) > 0:
            return "+{0}\n-{0}".format(
                self.name.capitalize() + "_Bonus"
                if (self.sDown + self.mod.sUp)
                else self.name.upper()
            )
        else:
            return ""


def get(string, l1, l2):
    string = (
        string.replace("\\\\", "__\\\\__")
        .replace("\\" + l1, "")
        .replace("\\" + l2, "")
        .replace("__\\\\__", "\\")
    )
    if l1 in string and l2 in string:
        i = string.find(l1)
        j = string.find(l2, i + 1)
        if min(i, j) == -1:
            return None
        return string[i + 1 : j]
    return None


def var(dic):
    u = dic.update

    def main(string):
        i = string.find(":")
        u({string[:i]: string[i + 1 : -1]})

    return main


def moods(lst, dct):
    l = lst.append
    d = dct.update

    def main(mod):
        d({mod.name: len(lst)})
        l(mod)

    return main


def openFile(fileName):
    arr = []
    modl = []
    modd = {}
    vrs = {}
    a = arr.append
    v = var(vrs)
    m = moods(modl, modd)
    m(modifyer("", "", ""))
    with open(fileName, "r") as f:
        for i in f:
            if i[0] in ["$", "|", "#"]:
                if i[0] == "$":
                    v(i)
                elif i[0] == "|":
                    t = modifyer(i)
                    if not None in [t.name, t.bind]:
                        m(t)
            else:
                a(i)
    for i in modl:
        if i.mod == None:
            i.mod = modl[0]
        else:
            i.mod = modl[modd.get(i.mod)]
            (i.mod.pred if i.d else i.mod.preu).append(i)

    for i in modl:
        if i.name != "":
            for j in i.mod.preu if i.d else i.mod.pred:
                j.nUp += i.sUp

    string = "".join(arr).replace("\\$", "__$\\__")
    for i in vrs:
        string = string.replace(i, vrs[i])
    arr = string.replace("__$\\__", "\\$").split("\n")
    plane = ""
    for i in arr:
        if "[" in i or "{" in i:
            down = True
            bind = get(i, "[", "]")
            if bind == None:
                bind = get(i, "{", "}")
                if bind != None:
                    down = False
            if bind != None:
                t = modd.get(bind)
                if t != None:
                    modl[t].add(i, down)
                else:
                    print "invalid name,", t
            else:
                print "Sorry I couldn't decifer the name from,", i
        elif ("`" in i or "(" in i) and ("'" in i or '"' in i):
            a = alias(i)
            plane += "{}\n".format(str(a))
        else:
            if i != "":
                plane += "{}\n".format(i)

    # print plane
    for i in modl:
        plane += "\n{!s}".format(i)
    for i in modl:
        plane += "{}\n".format(i.call())
    plane += "echo {}.cfg".format(fileName[:-4])
    print plane
    place = (
        "/home/peilonrayz/.local/share/Steam/SteamApps/common/dota 2 beta/dota/cfg/"
        + fileName[:-4]
        + ".cfg"
    )
    print place
    with open(place, "w") as f:
        f.write(plane)


# openFile('keybinds.txt')
# openFile('naga.txt')
# openFile('axe.txt')
openFile("test.txt")
