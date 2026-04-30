from enum import Enum

class Environment(str, Enum):
    dev = "dev"
    test = "test"
    prod = "prod"

class Format(str, Enum):
    dash = "dash"
    hls = "hls"

class SocialPlatforms(str, Enum):
    website = "website"
    instagram = "instagram"
    telegram = "telegram"
    x = "x"
