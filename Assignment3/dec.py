from oracle import *
import sys

'''
Assignment 3

Padding-oracle attack.
'''

def xor(a, b):     # xor two arrays of same lengths
	return [x^y for (x, y) in zip(a, b)]

def usage():
	print "Usage: python dec.py <filename>"
	sys.exit(-1)

L = 16      # block length
def decrypt(secret):   
	num_blocks = len(secret) / L
	print "[*] %d blocks" % num_blocks
	blocks = [secret[i*16:(i+1)*16] for i in range(0, 3)]

	# Decrypt last block
	iv = blocks[1][:]	# copy array
	
	# 1. Learn the number of padding bytes
	pad = 0xff
	for i in range(0, 15):
		iv[i] += 1

		data = blocks[0] + iv + blocks[2]
		rc = Oracle_Send(data, 3)
		if not rc:
			pad = L-i
			print "[+] Padding is %d" % pad
			break

	# 2. Learn the remaining bytes
	curr_guess = [0] * 16
	for i in range(L-pad, L, 1):
		curr_guess[i] = pad

	for i in range(L-pad-1, -1, -1):
		# Restore modified blocks
		blocks = [secret[idx*16:(idx+1)*16] for idx in range(0, 3)]
		iv = blocks[1][:]

		for p in range(i+1, L, 1):
			iv[p] = iv[p] ^ curr_guess[p] ^ (L-i)
			
		for j in range(0, 256):
			#print j
			iv[i] = j

			data = blocks[0] + iv + blocks[2]
			rc = Oracle_Send(data, 3)
			if rc:
				curr_guess[i] = (L-i) ^ j ^ blocks[1][i]
				print "[+] Block 2 guess: ", "".join(chr(b) for b in curr_guess).strip()
				break	
	
	msg = "".join([chr(b) for b in curr_guess])

	###### Guess first block (block 0 is the IV ######
	print "Guessing next blocks ...."
	curr_guess = [0] * 16

	for i in range(L-1, -1, -1):
		# Restore modified blocks
		blocks = [secret[idx*16:(idx+1)*16] for idx in range(0, 2)]
		iv = blocks[0][:]

		for p in range(i+1, L, 1):
			iv[p] = iv[p] ^ curr_guess[p] ^ (L-i)
			
		for j in range(0, 256):
			#print j
			iv[i] = j

			data = iv + blocks[1]
			rc = Oracle_Send(data, 2)
			if rc:
				# First time we get a correct padding, it was most probably 01
				curr_guess[i] = (L-i) ^ j ^ blocks[0][i]
				print "[+] Block 1 guess: ", "".join(chr(b) for b in curr_guess).strip()
				break	

	msg = "".join([chr(b) for b in curr_guess]) + msg
	print msg


if __name__ == "__main__":
	if len(sys.argv) < 2:
		usage()
	
	f = open(sys.argv[1])
	data = f.read()
	f.close()

	Oracle_Connect()

	decrypt([ord(c) for c in data.decode('hex')])

	Oracle_Disconnect()
	
	
''' 
3 blocks:
IV + b1 + b2

Data:
Yay! You get an A. =)

'''
