#!/usr/bin/python

'''
Assignment 2

Breaking the one-time pad (when the same key is used more than once)
'''

import sys

messages =[
"BB3A65F6F0034FA957F6A767699CE7FABA855AFB4F2B520AEAD612944A801E",
"BA7F24F2A35357A05CB8A16762C5A6AAAC924AE6447F0608A3D11388569A1E",
"A67261BBB30651BA5CF6BA297ED0E7B4E9894AA95E300247F0C0028F409A1E",
"A57261F5F0004BA74CF4AA2979D9A6B7AC854DA95E305203EC8515954C9D0F",
"BB3A70F3B91D48E84DF0AB702ECFEEB5BC8C5DA94C301E0BECD241954C831E",
"A6726DE8F01A50E849EDBC6C7C9CF2B2A88E19FD423E0647ECCB04DD4C9D1E",
"BC7570BBBF1D46E85AF9AA6C7A9CEFA9E9825CFD5E3A0047F7CD009305A71E"
]

def check_range(b):
        if (b >= 65 and b <= 90) or (b >= 97 and b <= 122) or (b == 0):
                return True
        return False

def strxor(a, b):     # xor two strings of different lengths
        if len(a) > len(b):
                return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
        else:
                return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


hex_c = [m.decode("hex") for m in messages]

# will build strem cipher here
stream = {}

# find (possible) blank spaces from each encrypted string
for i in range(0, len(hex_c)):
        letters_dict = {}
        for j in range(0, len(hex_c)):
                if j == i :
                        continue
                tmp = strxor(hex_c[i], hex_c[j])
                for k in range(0, len(tmp)):
                        if check_range(ord(tmp[k])):
                                if k in letters_dict :
                                        letters_dict[k] = letters_dict[k] + 1
                                else:
                                        letters_dict[k] = 1
        print "Possible spaces in message ", i
        for key in letters_dict.keys():
                if letters_dict[key] < len(messages)-2:
                        del letters_dict[key]
        print letters_dict
        print "Possible key bytes, from message ", i
        for key in letters_dict.keys():
                stream_byte = ord(hex_c[i][key]) ^ ord(" ")
                print "stream[%d] = %0d" % (key, stream_byte)
                stream[key] = stream_byte

# Manual adjusting (done later)
stream[0] = ord(messages[0].decode('hex')[0]) ^ ord('I')
stream[6] = ord(messages[5].decode('hex')[6]) ^ ord('s')
stream[8] = ord(messages[0].decode('hex')[8]) ^ ord('n')
stream[10] = ord(messages[0].decode('hex')[10]) ^ ord('i')
stream[17] = ord(messages[0].decode('hex')[17]) ^ ord('e')
stream[20] = ord(messages[0].decode('hex')[20]) ^ ord('e')
stream[29] = ord(messages[0].decode('hex')[29]) ^ ord('n')
stream[30] = ord(messages[3].decode('hex')[30]) ^ ord('?')


# Bonus: decrypt the 10 auxiliary messages
for msg in messages:
    target_dec = msg.decode('hex')
    target_v = [c for c in target_dec]

    for i in range(0, len(target_v)):
            if i in stream:
                    target_v[i] = ord(target_v[i]) ^ stream[i]
            else:
                    target_v[i] = ord(target_v[i])
    print "".join([chr(c) for c in target_v])
    

'''
Decrypted messages:

I am planning a secret mission.
He is the only person to trust.
The current plan is top secret.
When should we meet to do this?
I think they should follow him.
This is purer than that one is.
Not one cadet is better than I.

'''    
