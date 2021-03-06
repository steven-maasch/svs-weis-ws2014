#!/usr/bin/python2.7

# http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
# http://de.wikipedia.org/wiki/RSA-Kryptosystem
# http://www2.informatik.uni-hamburg.de/wsv/teaching/sonstiges/EwA-Folien/Sohst-Folien.pdf

import hashlib, base64
import logging
import binascii
from math import floor
from my_xtea import encrypt_cbc, decrypt_cbc

seperator = "-" * 80

def gen_dhke_key(base, exp, div):
	return base ** exp % div

def euclid(a, b):
	if b == 0:
		return a
	else:
		return euclid(b, a % b)

def extended_euclid(a, b):
	'''
	Taken from http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
	'''
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = extended_euclid(b % a, a)
	return (g, x - (b // a) * y, y) # // Floor Division

def mod_inv(a, m):
	'''
	Returns modular inverse if exisits else None 
	Taken from http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
	'''
	gcd, x, y = extended_euclid(a, m)
	if gcd != 1:
		return None
	else:
		return x % m

def rsa_cipher(msg, key, n):
	return msg ** key % n

def a1():
	# Aufgabe 1
	print seperator
	print "Aufgabe 1"
	print seperator
	p = 467
	g = 2
	rand_set = [(2, 5), (400, 134), (228, 57)]
	print "p = {}, g = {}".format(p, g)
	print seperator
	for a, b in rand_set:
		print "a = {}, b = {}".format(a, b)
		public_key_A = gen_dhke_key(g, a, p)
		print "A = {}".format(public_key_A)
		public_key_B = gen_dhke_key(g, b, p)
		print "B = {}".format(public_key_B)
		
		shared_key_B = gen_dhke_key(public_key_A, b, p)
		shared_key_A = gen_dhke_key(public_key_B, a, p)
		shared_key = gen_dhke_key(g, a * b, p)
		
		assert(shared_key == shared_key_A == shared_key_B)
		
		print "Shared key K_B = {}".format(shared_key_B)
		print "Shared key K_A = {}".format(shared_key_A)
		print "Shared key K = {}".format(shared_key)

def a2():
	# Aufgabe 2
	print seperator
	print "Aufgabe 2"
	print seperator
	p = 5
	q = 11
	e = 3
	msg = 9
	n = p * q
	phi_n = (p - 1) * (q - 1)

	# Calculate private exponent
	d = mod_inv(e, phi_n)
	print "Public key = ({}, {})".format(e, n)
	print "Private key = ({}, {})".format(d, n)

	encrypted_msg = rsa_cipher(msg, e, n)
	print "Plain message = {}".format(msg)
	print "Encrypted message = {}".format(encrypted_msg)
	print "Decrypted message = {}".format(rsa_cipher(encrypted_msg, d, n))

def a3():
	# Aufgabe 3
	print seperator
	print "Aufgabe 3"
	print seperator
	p = 41
	q = 17
	n = p * q
	phi_n = (p-1) * (q - 1)
	exps = [32, 39]
	for e in exps:
		if euclid(e, phi_n) == 1:
			print "Public exponent = {} -> Valid | Private exponent = {}".format(e, mod_inv(e, n))
		else:
			print "Public exponent = {} -> Invalid".format(e)

def main():
	logging.basicConfig(level=logging.ERROR)
	a1()
	a2()
	a3()
	# a4 -> naiveDH.py

if __name__ == "__main__":
	main()
