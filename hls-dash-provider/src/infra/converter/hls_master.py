
codecs = "mp4a.40.2"

def create_m3u8_content(
    bitrates: list[int],
) -> str:

    content = "#EXTM3U\n"
    content += "#EXT-X-VERSION: 7\n"
    content += "\n"
    for bitrate in bitrates:
        
        name = f"{bitrate//1000}k"
        
        content += (
            f'#EXT-X-STREAM-INF:'
            f' BANDWIDTH={bitrate},'
            f' VIDEO="NONE",'
            f' NAME="{name.upper()}",'
            f' CODECS="{codecs}"\n'
        )
        content += f"{name}.m3u8\n\n"
        
    return content.strip()