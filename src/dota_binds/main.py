import json

# alias
# bind
# bind
# bind


def loadCommand(data):
    return command(data[0], data[1], data[2])


def loadBind(data, key):
    return bind(loadCommand(data[0]), key, data[1], data[2])


def loadBKey(data, base=None):
    b = bKey(data[0], base)
    for i in data[1]:
        loadBind(i, b)
    return b


def loadBKeys(data, base):
    for i in data:
        loadBKey(i, base)


def loadCommandHolder(data):
    c = commandHolder()
    for i in data:
        c.add(loadCommand(i))
    return c


def loadForm(lst):
    b = bindHolder(loadBKey(lst[1]), loadCommandHolder(lst[0]))
    loadBKeys(lst[2], b)
    return b


class command(object):
    command = ""
    command2 = ""
    name = ""
    name2 = ""
    string = ""

    def __init__(self, name, command, command2=""):
        self.command = command
        self.command2 = command2
        self.name = name
        self.name2 = name

        if self.command2 != "":
            self.string += 'alias "+' + name + '" "' + self.command + '"\n'
            self.string += 'alias "-' + name + '" "' + self.command2 + '"'
            self.name = "+" + self.name
        else:
            self.string += 'alias "' + name + '" "' + self.command + '"'

    def saveForm(self):
        return [self.name2, self.command, self.command2]


class bind(object):
    command = None
    key = ""
    up = True
    string = ""
    name = ""

    def __init__(self, command, bKey, key, up=False):
        if type(bKey) == str:
            raise "Type Error! 'key' was ment to be an object of bKey."
        self.command = command
        self.key = key
        self.up = up
        if type(command) != str:
            command = command.name
        if up:
            bKey = bKey.getBase()
        self.name = "mod" + bKey.upper() + "_" + key.upper()
        self.string = (
            'alias "' + self.name + '" "bind ' + key.lower() + " " + command + '"'
        )
        if up:
            bKey.append(self)
        else:
            bKey.down.append(self)

    def saveForm(self):
        return [self.command.saveForm(), self.key, self.up]


class bKey(object):
    key = None
    down = None
    base = None
    down = None
    up = None

    def __init__(self, key, b=None):
        self.key = key
        if b == None:
            self.base = None
            self.up = []
        else:
            self.base = b.base
            b.add(self)
            self.down = []

    def upper(self):
        return self.key.upper()

    def getBase(self):
        if self.base != None:
            return self.base
        return self

    def getBinds(self):
        string = ""
        if self.base != None:
            string += self.get(self.down)
            string += (
                'alias "+mod'
                + self.upper()
                + '" "'
                + ";".join(i.name for i in self.down)
                + '"\n'
            )
            string += 'alias "-mod' + self.upper() + '" "none"\n'
            string += 'bind "' + self.upper() + '" "+mod' + self.upper() + '"'
        else:
            string += self.get(self.up)
            string += 'alias "none" "' + ";".join(i.name for i in self.up) + '"\n'
        return string

    def get(self, lst):
        string = ""
        for i in lst:
            string += i.command.string + "\n"
        for i in lst:
            string += i.string + "\n"

        return string

    def append(self, data):
        if self.base != None:
            self.base.append(data)
        else:
            self.up.append(data)

    def saveForm(self):
        if self.down != None:
            return [self.key] + [[i.saveForm() for i in self.down]]
        else:
            return [self.key] + [[i.saveForm() for i in self.up]]


class commandHolder(object):
    lst = None

    def __init__(self):
        self.lst = []

    def add(self, data):
        self.lst.append(data)

    def getData(self):
        return "\n".join(i.string for i in self.lst) + "\n"

    def saveForm(self):
        return [i.saveForm() for i in self.lst]


class bindHolder(object):
    lst = None
    base = None
    comm = None

    def __init__(self, b=None, c=None):
        self.lst = []
        if b == None:
            self.base = bKey("")
        else:
            self.base = b
        if c == None:
            self.comm = commandHolder()
        else:
            self.comm = c

    def getData(self):
        string = ""
        string += self.comm.getData()
        string += self.base.getBinds()
        string += "\n".join(i.getBinds() for i in self.lst)
        return string

    def add(self, data):
        self.lst.append(data)

    def saveForm(self):
        return (
            [self.comm.saveForm()]
            + [self.base.saveForm()]
            + [[i.saveForm() for i in self.lst]]
        )


b = bindHolder()
m4 = bKey("mouse4", b)
b.comm.add(command("sFollow", ""))
bind(
    command("top", "dota_camera_setpos -2296.339355 1085.593506 0.000000", "sFollow"),
    m4,
    "1",
)
bind(
    command("bot", "dota_camera_setpos 2874.552734 -3017.180664 0.000000", "sFollow"),
    m4,
    "1",
    True,
)
bind(command("tShop", "toggleshoppanel"), m4, "2")
bind(command("sToggle", "dota_smart_camera_toggle"), m4, "2", True)
bind(
    command(
        "home", "dota_select_courier;dota_ability_execute 0;+camera;dota_courier_burst"
    ),
    m4,
    "3",
)
bind(
    command(
        "secret",
        "dota_select_courier;dota_ability_execute 1;+camera;dota_courier_burst",
    ),
    m4,
    "3",
    True,
)
bind(command("courier", "dota_courier_deliver;dota_courier_burst"), m4, "4")
bind(command("burst", "dota_courier_burst"), m4, "4", True)
bind(command("sCourier", "dota_select_courier"), m4, "5")
bind(command("", ""), m4, "5", True)
bind(command("", ""), m4, "TAB")
bind(command("", ""), m4, "TAB", True)
bind(command("item0", "dota_item_execute 0"), m4, "a")
bind(command("item1", "dota_item_execute 1"), m4, "a", True)
bind(command("item2", "dota_item_execute 2"), m4, "s")
bind(command("item3", "dota_item_execute 3"), m4, "s", True)
bind(command("item4", "dota_item_execute 4"), m4, "d")
bind(command("item5", "dota_item_execute 5"), m4, "d", True)
m5 = bKey("mouse5", b)
bind(command("test", "test"), m5, "1")
item = b.saveForm()

b = loadForm(b.saveForm())
print item == b.saveForm()
