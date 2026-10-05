import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = (
            str(self.index)
            + str(self.timestamp)
            + json.dumps(self.data, sort_keys=True)
            + str(self.previous_hash)
        )

        return hashlib.sha256(block_content.encode()).hexdigest()


class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            "2026-01-01 00:00:00",
            {
                "type": "Genesis Block",
                "message": "LandChain Blockchain Started"
            },
            "0"
        )

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            str(datetime.now()),
            data,
            latest_block.hash
        )

        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_chain(self):
        return self.chain
