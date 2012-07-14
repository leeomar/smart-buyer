
LOG_FILE = "../log/server.log"

MODULES = {
    "modules.ipo.IPOModule" : 30,
    #"modules.BaseModule" : 10, 
    #"modules.BaseRuleModule" : 20,
    #"modules.example.ExampleModule" : 60,
}

RULES = {
    #"BaseRuleModule" :
    #    (
    #        "modules.rule.BaseRule",
    #    ),
    #"ExampleModule" :
    #    (
    #        "modules.example.ExampleRule",
    #    ),
    "IPOModule" :
        (
            "modules.ipo.IPORule",
        ),
}

#ExampleRule = {
#    "param" : 1,
#}

DEFAULT_REDIS = {
    "host" : "192.168.23.211",
    "port" : 6379,
    "db" : 2,
    "expire" : 3600, #1h
}

ORACLE = {
    "host" : "172.20.23.104",
    "port" : 1521,
    "sid"  : "odb",
    "user" : "db40",
    "pwd"  : "db40"
}
