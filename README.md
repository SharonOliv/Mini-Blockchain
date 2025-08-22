# Mini-Blockchain
A simple blockchain implementation in Python that simulates a cryptocurrency called **Olives**.  
This project demonstrates how a blockchain works by maintaining a ledger of users, balances, and transactions.  

## Features
- Create a new blockchain with a **Genesis Block**.
- Add new **users** with an initial balance (in Olives).
- Make **transactions** between users.
  - Valid transactions update balances and are added to the blockchain.
  - Invalid transactions (e.g., insufficient balance, non-existing users) are rejected.
- Print the blockchain with block details (hash, previous hash, transactions).
- Verify if the blockchain is valid.

## Tech Used
- Python 3
- Built-in libraries: `hashlib`, `json`, `time`

## How It Works
1. Start the program.
2. Add users and give them some Olives.
3. Make transactions between users.
   - If valid → added to a new block.
   - If invalid → rejected.
4. Print the blockchain to see the chain of blocks.
5. Check validity of the chain anytime.

## Example Usage
```bash
--- Olives Blockchain Menu ---
1. Add User
2. Show Users
3. Make Transaction
4. Show Blockchain
5. Check Validity
6. Exit
```
