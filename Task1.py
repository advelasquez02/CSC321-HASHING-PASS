from Crypto.Hash import SHA256

#hash and return hex form
def hashSHA256(string):
    #turn in literal byte form
    string = string.encode('utf-8')
    return SHA256.new(string).hexdigest()


if __name__ == '__main__':
    while True:
        string = input('Enter a string (press q to quit): ')
        if string == 'q':
            break
        print(hashSHA256(string))


