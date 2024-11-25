import time


def get_duration(duration: int) -> str:
    if duration < 3600:
        return time.strftime("%M:%S", time.gmtime(duration))
    else:
        return time.strftime("%H:%M:%S", time.gmtime(duration))


def get_formatted_duration(duration: int) -> str:
    if duration < 3600:
        time_str = time.strftime("%M:%S", time.gmtime(duration))
        time_split = time_str.split(":")
        return str(int(time_split[0])) + " min " + str(int(time_split[1])) + " sec "
    else:
        time_str = time.strftime("%H:%M", time.gmtime(duration))
        time_split = time_str.split(":")
        return str(int(time_split[0])) + " h " + str(int(time_split[1])) + " min "
