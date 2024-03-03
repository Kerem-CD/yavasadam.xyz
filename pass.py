import bcrypt
password = b"1234"
# Generate a salt

# Hash the password
hashed_password = bcrypt.hashpw(password, b'$2b$12$3whq2NeGvsWq7CtNcWWhB.')
print(hashed_password)