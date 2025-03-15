import time

# Cache dictionary
_cache = {}

def cache_set(key, value, ttl: int = 300):
    """
    Set a value in the cache with TTL.
    """
    expire_at = time.time() + ttl if value is not None else 0
    _cache[key] = {"value": value, "expire_at": expire_at}

def cache_get(key):
    """
    Retrieve a value from the cache if not expired.
    """
    data = _cache.get(key)
    if data and data["expire_at"] > time.time():
        return data["value"]
    # Cache miss or expired
    if key in _cache:
        del _cache[key]
    return None
