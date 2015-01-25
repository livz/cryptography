#!/usr/bin/env python

from oracle import *
import sys

def strxor(a, b):     # xor two strings of same length
	return "".join([chr(ord(x)^ord(y)) for (x, y) in zip(a, b)])
	
data = "I, the server, hereby agree that I will pay $100 to this student"
Oracle_Connect()

# Tag for the first 2 blocks - b1, b2
tag1 = Mac(data[:32], 32)
print "[*] Tag B1, B2: %s (%d)" % (str(tag1).encode("hex"), len(tag1))

# tag for tag1^b3, b4
new_b1 = strxor(str(tag1), data[32:48])
print "[*] Tag1^B3: %s (%d)" %  (new_b1.encode("hex"), len(new_b1))
tag2 = Mac(new_b1 + data[48:64], 32)
print "[*] Tag2 for tag1^B3, B4: %s (%d)" %  (str(tag2).encode("hex"), len(tag2))

ret = Vrfy(data, len(data), tag2)

if (1 == ret):
    print "[+] Message verified successfully!"
elif (0 == ret):
    print "[-] Message verification failed."
else: 
    print "[-] Refused to check the message (invalid length)"

Oracle_Disconnect()

''' 
Answer:
DC315A27
'''
