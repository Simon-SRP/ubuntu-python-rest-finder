def validate_url(url):
    """Проверяет, является ли строка допустимым URL"""
    return url.startswith(('http://', 'https://'))