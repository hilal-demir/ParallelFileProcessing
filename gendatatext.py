#!/usr/bin/python3
#
#               NOTICE
#      COPYRIGHT 2019 AB INITIO
# UNPUBLISHED -- ALL RIGHTS RESERVED
#
# This program is confidential and a trade secret of Ab Initio.
# Receipt or possession conveys no rights for any purpose without
# specific written consent from Ab Initio.
#
import random
import datetime

"""
Generate test CSV files in the current working directory.
Each file will have a different (random) number of records.
"""

NUM_FILES = 100
MIN_FILE_LENGTH = 1000
MAX_FILE_LENGTH = 10000
MAX_CUST_ID = 100000

transid = 0


def randdate(limit):
    """
    Return a random date between 1 Jan 2000 and limit days in the future.
    """
    return datetime.date(2000, 1, 1) + datetime.timedelta(days=random.randint(0, limit))


def write_file(filename):
    """
    Create a file with a given filename and a random number of records and data.
    """
    with open(filename, "w") as out:
        global transid
        for i in range(0, random.randint(MIN_FILE_LENGTH, MAX_FILE_LENGTH)):
            transid = transid + 1
            transtype = "P"
            transdate = randdate(1000)
            custid = random.randint(0, MAX_CUST_ID)
            quantity = random.randint(1, 10)
            price = random.random() * 100
            discount = random.random() * 10
            returnid = ""
            reason = ""
            print(
                "{transid},{transtype},{transdate},{custid},{quantity},{price:.2f},{discount:.2f},{returnid},{reason}".format(
                    transid=transid, transtype=transtype, transdate=transdate, custid=custid, quantity=quantity,
                    price=price, discount=discount, returnid=returnid, reason=reason), file=out)


if __name__ == "__main__":
    for i in range(0, NUM_FILES):
        print("Generating file {}".format(i))
        write_file("transactions_" + str(i) + ".dat")