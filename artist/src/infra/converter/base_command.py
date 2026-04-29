from urllib.parse import urlparse

def is_valid_url(
    url: str,
) -> bool:
    
    result = urlparse(url)
    return all(
        [
            result.scheme,
            result.netloc,
        ],
    )

def base_command(
    input_url: str,
    log: bool = False,
) -> list:
        
    command = ["ffmpeg", "-y"]
    
    if not log:
        command += ["-loglevel", "quiet"]
    
    if "pipe" in input_url:
        command += ["-i", "pipe:0"]
        
    elif is_valid_url(input_url):
        command += [
            '-reconnect', '1',              # Enables reconnection attempts if a network error occurs during opening or reading.
            '-reconnect_at_eof', '1',       # Forces reconnection if the connection is lost at the end of the file (prevents premature exit).
            '-reconnect_streamed', '1',     # Allows reconnection for non-seekable or streamed HTTP resources (like S3 links).
            '-reconnect_delay_max', '5',    # Wait up to `n` seconds before trying to connect again.
            "-timeout", str(5_000_000),     # Give up and close the program if it can't connect within `n` seconds.
            "-i", input_url,
        ]
        
        # "-use_template", "1",
        # "-use_timeline", "1",
        # "write_seg_list", "-1",
        # "-thread_queue_size", str(16 * 1024),
        
    return command
        
def base_audio_command(
    bitrate: int,
):
    
    command = [
        "-vn",
        "-map", "0:a",
        "-c:a", "aac",
        "-b:a", str(bitrate),
    ]
    
    return command