import yaml


class ConfigParser(object):
    def __init__(self):
        self.pegasus_hosts = None

    def parse(self, config_file, env):
        with open(config_file) as f:
            conf = yaml.load(f.read())
            self.pegasus_hosts = conf['pegasus_hosts']
            for k, v in conf[env.lower()].items():
                self.__dict__[k] = v
