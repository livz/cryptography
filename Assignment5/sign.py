from oracle import *
from helper import *

'''
Assignment 5

Attacking an RSA-based signature scheme
'''

MAX_MSG_LEN = 504

# Transforms m => (0..0m | 0..0m)
def transform(m):
    return bin(m)[2:].zfill(MAX_MSG_LEN + 8) + bin(m)[2:].zfill(MAX_MSG_LEN + 8)
    
n = 119077393994976313358209514872004186781083638474007212865571534799455802984783764695504518716476645854434703350542987348935664430222174597252144205891641172082602942313168180100366024600206994820541840725743590501646516068078269875871068596540116450747659687492528762004294694507524718065820838211568885027869

e = 65537

Oracle_Connect()

msg = "Crypto is hard --- even schemes that look complex can be broken"
m = ascii_to_int(msg)

s = Sign(1)			# (2^512 + 1)^d mod N
m1, m2 = 2, m/2		# m = m1 * m2
s1 = Sign(m1)		# (m1(2^512+1))^d
s2 = Sign(m2)		# (m1(2^512+1))^d

sigma = (s1 * s2 * modinv(s, n)) % n

if Verify(m, sigma):
	print "[*] Found correct signature:", hex(sigma).upper()[2:]
else:
	print "[-] Invalid signature."	

Oracle_Disconnect()

'''
N - module
d - private key
e - exponent = 10001(h) = 65537 = 2^16 + 1

m - 63 bytes
M = 0x00 m 0x00 m = m * (2^512 +1)
M - 128 bytes

Sign:
sigma =  M^d mod N

Verify:
M = sigma^e mod N

Solution:
m = m1*m2 = 2 * m/2
M = m1*m2*(2^512+1)
S = sign(M) = M^d = m1^d * m2^d * (2^512+1)^d

s = sign(1) = (2^512+1)^d
s1 = sign(2) = sign(m1) = (m1(2^512+1))^d
s2 = sign(m/2) = sign(m2) = (m2(2^512+1))^d

Final signature for M:
S = s1 * s2 * s^(-1)  mod N
'''
