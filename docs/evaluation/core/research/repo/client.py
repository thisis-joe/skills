REQUEST_TIMEOUT_MS = 300

def request(client, url):
    return client.get(url, timeout=REQUEST_TIMEOUT_MS / 1000)
