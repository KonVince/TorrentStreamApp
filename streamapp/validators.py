from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_magnet_uri(value):
    try:
        parsed = urlparse(value)
        if parsed.scheme != 'magnet':
            raise ValidationError('The URL scheme must be "magnet".')
        if not parsed.query:
            raise ValidationError('The magnet URI must have a query string.')
        params = dict(map(lambda x: x.split('='), parsed.query.split('&')))
        if 'xt' not in params or not params['xt'].startswith('urn:btih:'):
            raise ValidationError('Invalid magnet URI format.')
    except ValueError:
        raise ValidationError('Invalid magnet URI format.')