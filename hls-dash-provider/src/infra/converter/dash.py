from .base_command import base_command, base_audio_command
import platform
from pathlib import Path

def dash_command(
    temp: str,
    input_url: str,
    bitrate: int,
    log: bool = False
):
        
    relpath = platform.system() in ["Linux"]
    
    temp_path = Path(temp)    
    m4s_path = temp_path / f"{bitrate//1000}k.m4s"
    mpd_path = temp_path / f"{bitrate//1000}k.mpd"
    
    single_file_name = m4s_path.name if relpath else m4s_path
    
    command = base_command(input_url, log)
    command += base_audio_command(bitrate)
    
    command += [
        "-f", "dash",
        "-adaptation_sets", "id=0,streams=a",
        "-single_file", "1",
        "-single_file_name", single_file_name,
        str(mpd_path),
    ]
    
    return command, m4s_path, mpd_path