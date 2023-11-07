from flask_caching import Cache

# setting up the disk cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': './cache',
    "CACHE_DEFAULT_TIMEOUT": 0
    # ^^ never expires
}
cache = Cache()
