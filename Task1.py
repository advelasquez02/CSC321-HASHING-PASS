from Crypto.Hash import SHA256
import time



#hash and return hex form
def hashSHA256(string):
    #turn in literal byte form
    string = string.encode('utf-8')
    return SHA256.new(string).hexdigest()

#truncate the to the first 8 bits
def hashSHA256Trunc(string, num_bits):
    string = string.encode("utf-8")
    h = SHA256.new(string).digest()

    num_bytes = (num_bits + 7) // 8
    value = int.from_bytes(h[:num_bytes], "big")

    extra_bits = (num_bytes * 8) - num_bits
    return value >> extra_bits



def findCollision(num_bits):
    checkedStrings = {}
    i = 0

    start = time.time()

    while True:
        msg = "msg_" + str(i)
        hashNum = hashSHA256Trunc(msg, num_bits)

        if hashNum in checkedStrings:
            end = time.time()
            elapsed = end - start
            inputs = i + 1

            return inputs, elapsed

        checkedStrings[hashNum] = msg

        if i % 1000000 == 0 and i != 0:
            print(f"Checked {i} messages...")

        i += 1



if __name__ == '__main__':
    results = []

    for bits in range(8, 51, 2):
        inputs, elapsed = findCollision(bits)
        results.append((bits, inputs, elapsed))
        print(bits, inputs, elapsed)


