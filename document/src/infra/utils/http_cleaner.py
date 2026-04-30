def clean_outbound_request(data: dict | None) -> dict:
    """Remove None values before sending HTTP requests."""
    return {k: v for k, v in (data or {}).items() if v is not None}
