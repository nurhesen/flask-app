from fastapi import Request, HTTPException, status


async def validate_payload_size(request: Request, max_size: int):
    """
    Validates that the request body does not exceed max_size bytes.
    """
    body = await request.body()
    if len(body) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload exceeds maximum size of {max_size} bytes"
        )
