import re

template = f"""
<?xml version="1.0" encoding="utf-8"?>
<MPD

 	type="static"
  
	mediaPresentationDuration="duration_place">
	
 	<Period id="0" start="PT0.0S">
		<AdaptationSet id="0" contentType="audio" startWithSAP="1" segmentAlignment="true" bitstreamSwitching="true">
        	representations_place
		</AdaptationSet>
	</Period>
 
</MPD>
"""

def parse_pt(duration):
    match = re.fullmatch(r'PT(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+(?:\.\d+)?)S)?', duration)
    if not match:
        return None
    h = float(match.group('h') or 0)
    m = float(match.group('m') or 0)
    s = float(match.group('s') or 0)
    return h * 3600 + m * 60 + s

def create_mpd_content(
    PTMS_list: list[str],
    reprs: list[str],
) -> str:
    
    representations = "\n			".join(reprs)
    
    return template.replace(
        "duration_place",
        max(PTMS_list, key=parse_pt),
    ).replace(
        "representations_place",
        representations,
    ).strip()