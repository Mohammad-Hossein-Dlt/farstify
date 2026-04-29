from .base_command import base_command, base_audio_command
import platform
from pathlib import Path

def hls_command(
    temp: str,
    input_url: str,
    bitrate: int,
    log: bool = False
):
    relpath = platform.system() in ["Linux"]
    relpath = False
    
    temp_path = Path(temp)
    ts_path = temp_path / f"{bitrate//1000}k.ts"
    m3u8_path = temp_path / f"{bitrate//1000}k.m3u8"
    
    hls_segment_filename = ts_path.name if relpath else ts_path
    
    command = base_command(input_url, log)
    command += base_audio_command(bitrate)
    
    command += [
        "-f", "hls",
        "-hls_list_size", "0",
        "-hls_flags", "single_file",
        "-master_pl_name", "master.m3u8",
        "-hls_segment_filename", hls_segment_filename,
        m3u8_path,
    ]
    
    return command, ts_path, m3u8_path