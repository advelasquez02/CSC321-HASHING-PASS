# import nltk
import time

import nltk
from bcrypt import *
from nltk.corpus import words
#uncomment and run this before first run
nltk.download("words")
from multiprocessing import Pool


#for each user you must
#1) get its hash and salt
#2) iterate through the list of words + hash
#3) check to see it's in the dictionary, return the password found

# filter words, making sure we only have words of length >= 6 and <= 10
def validWords(word_list):
    filtered = [w.lower() for w in word_list if 6 <= len(w) <= 10 and w.isalpha()]
    return filtered

def parseUsers(userString):
    userName, fullHash = userString.strip().split(":")
    salt = fullHash[:29]
    return userName, salt.encode("UTF-8"), fullHash.encode("UTF-8")

def crackOneUser(args):
    username, salt, fullHash, word_list = args

    for word in word_list:
        if hashpw(word.encode("UTF-8"), salt) == fullHash:
            return username, word

    return username, None

def crackPass():
    word_list = validWords(words.words())

    users = []
    with open("shadow.txt", "r") as f:
        for line in f:
            username, salt, fullHash = parseUsers(line)
            users.append((username, salt, fullHash, word_list))

    with Pool() as pool:
        #creates processes and runs the given function on the user list
        results = pool.map(crackOneUser, users)

    for username, password in results:
        if password is not None:
            print("Cracked password! User: " + username + " Password: " + password)
        else:
            print("Password not found for user: " + username)

if __name__ == "__main__":
    start = time.time()
    crackPass()
    end = time.time()

    print("Runtime:", round(end - start, 2), "seconds")
    print("Runtime:", round((end - start) / 60, 2), "minutes")



