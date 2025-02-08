import enum

null_values = ["null", "Null", "NULL", "none", "None", "NONE"]
true_values = ["true", "True", "TRUE", "t", "T"]
false_values = ["false", "False", "FALSE", "f", "F"]


class ProcessActionTaskState(str, enum.Enum):
    launching = "launching"
    in_process = "in_process"
    completed = "completed"
    cancelled = "cancelled"
    error = "error"


class Directories(str, enum.Enum):
    temp = "temp/"


class DocumentQualities(str, enum.Enum):
    q64k_bit = "64k"
    q128k_bit = "128k"
    q256k_bit = "256k"
    q320k_bit = "320k"
    preview = "preview"

    @classmethod
    def directories(cls):
        return [
            cls.q64k_bit,
            cls.q128k_bit,
            cls.q256k_bit,
            cls.q320k_bit,
            cls.preview,
        ]

    @classmethod
    def qualities(cls):
        exclusions = [cls.preview]
        return [q.value for q in DocumentQualities.directories() if q not in exclusions]


class AgentRolesEntities(str, enum.Enum):
    Main_Artist = "Main_Artist"
    Featured_Artist = "Featured_Artist"
    Producer = "Producer"
    Composer = "Composer"
    Writer = "Writer"


class AccountTypes(str, enum.Enum):
    artist = "artist"
    user = "user"


class ContentTypes(str, enum.Enum):
    music = "music"
    podcast = "podcast"


class SortBy(enum.Enum):
    artist = "artist"
    title = "title"
    default = "default"


class OrderBy(enum.Enum):
    desc = "desc"
    asc = "asc"


class Socials(enum.Enum):
    website = "website"
    instagram = "instagram"
    telegram = "telegram"
    x = "x"
