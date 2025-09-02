import hashlib
import json
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # list of dicts
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.users = {}  # user: {balance, private_key, public_key}

    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), transactions, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}\n")

    # --- New Features ---
    def add_user(self, name, balance):
        if name in self.users:
            print("User already exists!")
            return

        # Generate RSA key pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        self.users[name] = {
            "balance": balance,
            "private_key": private_key,
            "public_key": public_key
        }
        print(f"User {name} added with {balance} Olives")

    def sign_transaction(self, sender, transaction_data):
        private_key = self.users[sender]["private_key"]
        signature = private_key.sign(
            transaction_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, public_key, transaction_data, signature):
        try:
            public_key.verify(
                signature,
                transaction_data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def make_transaction(self, sender, receiver, amount):
        if sender not in self.users or receiver not in self.users:
            print(" Invalid users!")
            return False

        if self.users[sender]["balance"] < amount:
            print("Transaction failed: insufficient balance")
            return False

        # prepare transaction data
        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "currency": "Olives",
            "timestamp": time.time()
        }
        tx_string = json.dumps(tx, sort_keys=True)

        # sign with sender's private key
        signature = self.sign_transaction(sender, tx_string)

        # attach signature and public key
        tx["signature"] = signature.hex()
        tx["public_key"] = self.users[sender]["public_key"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        # verify before adding
        pub_key = serialization.load_pem_public_key(
            tx["public_key"].encode(),
            backend=default_backend()
        )

        if not self.verify_signature(pub_key, tx_string, bytes.fromhex(tx["signature"])):
            print("Transaction signature invalid!")
            return False

        # update balances
        self.users[sender]["balance"] -= amount
        self.users[receiver]["balance"] += amount

        # add to blockchain
        self.add_block([tx])
        print("Transaction successful and added to block")
        return True

    def show_users(self):
        print("\n--- User Balances ---")
        for user, data in self.users.items():
            print(f"{user}: {data['balance']} Olives")
        print("---------------------\n")


if __name__ == "__main__":
    my_chain = Blockchain()

    while True:
        print("\n--- Olives Blockchain Menu ---")
        print("1. Add User")
        print("2. Show Users")
        print("3. Make Transaction")
        print("4. Show Blockchain")
        print("5. Check Validity")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            balance = int(input("Enter starting balance: "))
            my_chain.add_user(name, balance)

        elif choice == "2":
            my_chain.show_users()

        elif choice == "3":
            sender = input("Sender: ")
            receiver = input("Receiver: ")
            amount = int(input("Amount of Olives: "))
            my_chain.make_transaction(sender, receiver, amount)

        elif choice == "4":
            my_chain.print_chain()

        elif choice == "5":
            print("Is blockchain valid?", my_chain.is_chain_valid())

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")
