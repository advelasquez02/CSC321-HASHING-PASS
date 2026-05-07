import time
from multiprocessing import Pool
from bcrypt import hashpw
from nltk.corpus import words


def validWords(word_list):
    return [w.lower() for w in word_list if 6 <= len(w) <= 10 and w.isalpha()]


def parseUsers(userString):
    userName, fullHash = userString.strip().split(":")
    salt = fullHash[:29]
    return userName, salt.encode("UTF-8"), fullHash.encode("UTF-8")


def chunkList(word_list, num_chunks):
    chunk_size = len(word_list) // num_chunks

    chunks = []
    for i in range(0, len(word_list), chunk_size):
        chunks.append(word_list[i:i + chunk_size])

    return chunks


def crackChunkForUser(args):
    username, salt, fullHash, word_chunk = args

    for word in word_chunk:
        if hashpw(word.encode("UTF-8"), salt) == fullHash:
            return username, word

    return username, None


def crackPass():
    word_list = validWords(words.words())

    users = []
    with open("shadow.txt", "r") as f:
        for line in f:
            users.append(parseUsers(line))

    with Pool() as pool:
        num_processes = pool._processes
        chunks = chunkList(word_list, num_processes)

        for username, salt, fullHash in users:
            tasks = [(username, salt, fullHash, chunk) for chunk in chunks]

            results = pool.map(crackChunkForUser, tasks)

            for result_username, password in results:
                if password is not None:
                    print("Cracked password! User: " + result_username + " Password: " + password)
                    break


if __name__ == "__main__":
    start = time.time()
    crackPass()
    end = time.time()

    print("Runtime:", round(end - start, 2), "seconds")
    print("Runtime:", round((end - start) / 60, 2), "minutes")