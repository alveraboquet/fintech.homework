import hashlib

# output sha256 hash in hexadecimal string format
def hash(message):
    return hashlib.sha256(message).hexdigest()

# modify these messages
# note: we include the "b" before the string definition in order to represent it as bytes instead of a string
message_one = b"Hello world!"

message_two = b"Hello world!!"

# print both messages and their corresponding hashes
print(message_one, hash(message_one))
print(message_two, hash(message_two))

# compare the hashes in an if/else statement

hash_one = hash(message_one)

hash_two = hash(message_two)

if (hash_one == hash_two):
    print("Equal")
else:
    print("Not equal")

# compare the length of the hashes

print(f'Lenght of hash 1 {len(hash_one)}')
print(f'Lenght of hash 2 {len(hash_two)}')
