article_page_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

def get_exception_message(e):
    if hasattr(e, 'message'):
        return e.message
    else:
        return e