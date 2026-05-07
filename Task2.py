# import nltk
import time
from bcrypt import *
from nltk.corpus import words
#uncomment and run this before first run
# nltk.download("words")
import os
print(os.cpu_count())

#for each user you must
#1) get its hash and salt
#2) iterate through the list of words + hash
#3) check to see it's in the dictionary, return the password found

# filter words, making sure we only have words of length >= 6 and <= 10
def validWords(word_list):
    filtered = [w.lower() for w in word_list if 6 <= len(w) <= 10 and w.isalpha()]
    return filtered

def parseUsers(userString):
    userName, fullHash = userString.split(":")
    salt = fullHash[:29]
    return userName, salt.encode("UTF-8"), fullHash.encode("UTF-8")

def crackPass():
    word_list = validWords(words.words())
    with open("shadow.txt", "r") as f:
        for line in f:
            line = line.strip()  # removes newline \n

            #parses for the current user
            username, salt, fullHash = parseUsers(line)

            for word in word_list :
                if hashpw(word.encode("UTF-8"), salt) == fullHash:
                    print("Cracked password! User: " + username + " Password: " + word)
                    break
    return "Cracked all passwords!"

if __name__ == "__main__":
    start = time.time()
    crackPass()
    end = time.time()

    print("Runtime:", round(end - start, 2), "seconds")
    print("Runtime:", round((end - start) / 60, 2), "minutes")


