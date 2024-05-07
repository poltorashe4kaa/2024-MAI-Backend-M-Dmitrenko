class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.cache = {}

    def get(self, key: str) -> str:
        temp_value = self.cache.pop(key, "")
        if len(temp_value):
            self.cache[key] = temp_value
        return temp_value

    def set(self, key: str, value: str) -> None:
        if len(self.cache) == self.capacity:
            (k := next(iter(self.cache)), self.cache.pop(k))
        self.cache[key] = value

    def rem(self, key: str) -> None:
        self.cache.pop(key)