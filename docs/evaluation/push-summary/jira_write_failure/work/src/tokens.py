def expired(now, expires_at):
    return now >= expires_at

class TokenFamily:
    def __init__(self):
        self.current = "token-0"
        self.used = set()
        self.revoked = False
        self.sequence = 0

    def rotate(self, supplied):
        if supplied in self.used:
            self.revoked = True
            raise ValueError("reused token")
        if self.revoked or supplied != self.current:
            raise ValueError("invalid token")
        self.used.add(supplied)
        self.sequence += 1
        self.current = f"token-{self.sequence}"
        return self.current
