from context_objects import USER_DEFAULT_SETTINGS, USER_SETTINGS_MASK, USER_SETTINGS_FIELDS


class Settings:
    ENCODERS = {}
    @staticmethod
    def encoder(field):
        def wrapper(function):
            Settings.ENCODERS[field] = function
            return function
        return wrapper

    DECODERS = {}
    @staticmethod
    def decoder(field):
        def wrapper(function):
            Settings.DECODERS[field] = function
            return function
        return wrapper
    
    
    @staticmethod
    def encode_settings(settings):
        def mask_to_offset(mask):
            c = 1
            while (mask & c == 0):
                c = c << 1
            return c
        output = 0
        for key, value in settings:
            output += Settings.ENCODERS[key](value) * mask_to_offset(USER_SETTINGS_MASK[key])
        return output
    
    @staticmethod
    def decode_settings(code):
        def lstrip_code(mask, val):
            while (mask & 1 == 0):
                mask = mask >> 1
                val = val >> 1
            return val
        settings = {}
        for f in USER_SETTINGS_FIELDS:
            settings[f] = Settings.DECODERS[f](USER_SETTINGS_MASK[f], 
                                               lstrip_code(code & USER_SETTINGS_MASK[f]))
        return settings

    def __init__(self, settings=USER_DEFAULT_SETTINGS):
        self.settings = settings
    
    @classmethod
    def decode(cls, code):
        return cls(Settings.decode_settings(code))
    
    def encode(self):
        return Settings.encode_settings(self.settings)
        
@Settings.encoder('theme')
def _theme_encode(inp):
    if inp == 'dark':
        return 0b0
    elif inp == 'light':
        return 0b1
    else:
        return 0b0

@Settings.decoder('theme')
def _theme_decode(inp):
    if inp == 0b0:
        return 'dark'
    elif inp == 0b1:
        return 'light'
    else:
        return 'dark'