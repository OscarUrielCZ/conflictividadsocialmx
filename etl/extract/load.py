import yaml

yaml.warnings({'YAMLLoadWarning': False})
__data = None

def load_file(filename):
    """Loads a YAML file. WARNING: Check for yaml.load() deprecation"""
    global __data
    if not __data:
        with open(filename, mode='r') as f:
            __data = yaml.load(f, Loader=yaml.SafeLoader)
    return __data