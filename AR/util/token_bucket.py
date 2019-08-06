import asyncio
import time

class TokenBucket():
    """
    A basic token bucket used for throttling requests
    """
    def __init__(self, max_tokens, refill_rate):
        """
        max_tokens: how many tokens the bucket holds
        refill_rate: how many tokens / second are added
        """
        self.max_tokens = max_tokens
        self.time_quantum = 1.0 / refill_rate # time between tokens being added
        self.curr_tokens = max_tokens
        self.last_time = time.monotonic()

    def update(self):
        """
        See if enough time has passed and if so put tokens in the bucket
        """
        curr_time = time.monotonic()
        time_diff = curr_time - self.last_time
        if time_diff > self.time_quantum:
            self.curr_tokens += int(time_diff / self.time_quantum)
            if self.curr_tokens > self.max_tokens:
                self.curr_tokens = self.max_tokens
            self.last_time = curr_time
        
    async def get(self):
        """
        Wait for tokens to be available and then take one out
        """
        while (self.curr_tokens == 0):
            asyncio.wait(self.time_quantum)
            self.update()
        self.curr_tokens -= 1
        return
