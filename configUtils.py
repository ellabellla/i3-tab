import configparser

def load(path):
    config = configparser.ConfigParser()
    
    read = None
    try:
        read = config.read(path)
    except configparser.ParsingError as e:
        print(f"Couldn't parse config file: {e.message}")
        return None
    
    if len(read) == 0:
        print(f"Couldn't load config: {path}\n")
        return None
    
    if  'window' in config and \
        'color' in config['window'] and \
        'bcolor' in config['window'] and \
        'width' in config['window'] and \
        'selection' in config  and \
        'height' in config['selection']  and \
        'width' in config['selection']  and \
        'font' in config and \
        'selected' in config['font'] and \
        'unselected' in config['font']:
            return config
    else:
        print(f"Config is missing settings.\n")
        return None
    
    