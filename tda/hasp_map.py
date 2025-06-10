# tda/hasp_map.py

class HashMap:
    def __init__(self, capacity=100):
        self._capacity = capacity
        self._table = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % self._capacity

    def set(self, key, value):
        index = self._hash(key)
        bucket = self._table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self._table[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        index = self._hash(key)
        bucket = self._table[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

    def contains(self, key):
        return self.get(key) is not None

    def keys(self):
        return [k for bucket in self._table for (k, _) in bucket]

    def values(self):
        return [v for bucket in self._table for (_, v) in bucket]

    def items(self):
        return [(k, v) for bucket in self._table for (k, v) in bucket]
