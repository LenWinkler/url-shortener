from url.models import Url

def url_hash_exists(hashed_url):
    try:
        obj = Url.objects.get(url_hash=hashed_url)
    except Url.DoesNotExist:
        obj = None
    return obj