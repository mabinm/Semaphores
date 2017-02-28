#Final commit
#2_disc_golf_range.py - MP3 -Assignment 1
#This program was run using Python 3.4 and executed using command prompt
#Algorithm followed:
#1)Get input on number of frolfers, bucketsize and stash in total
#2)initiate cart and frolfer threads
#3)cart will wait on collecting till a frolfer does not have enough in stash to collect
#4)frolfer starts to pick from stash and throw
#5)When a frolfer doesnt have enough discs to satisfy the bucketsize, cart is sent out for collection
#6)At this time no frolfer can throw a disc. Cart collects the discs that have been thrown in the field so far
#7)if cart find that number of discs on field is less than the required bucketsize, it allows frolfers to start throwing for a random time
#Reference was made to code present online for understanding purposes
#Replaced lock mechanisms with semaphores for access to stash and control of discs thrown in field
#included code to ensure when cart collects less than the 
#required bucketsize, it allows frolfers to throw for a random time and then collect till cart has enough for a frolfer to pick

from threading import Semaphore, Lock, Thread
import random
import time
import sys

rng = random.Random()
rng.seed(100)

#initialization of variables and semaphores
stash = 0 
discs_on_field = 0
cart_collect = Semaphore(0) # wait for stash to be insufficient for frolfer
stash_full = Semaphore(0) #for stash protection
stash_access = Semaphore(1) # frolfers stash access semaphore
disc_growth = Semaphore(1) #semaphore to control frolfer throwing discs on field

def frolfer(discs, id):
	global stash
	global discs_on_field
	while True:
		print("Frolfer ", id , " calling for bucket")
		stash_access.acquire() #only one frolfer can pick up discs at a time
		if (stash < discs): #if insufficient discs in stash
			cart_collect.release(); #call for cart
			stash_full.acquire() #no frolfer can pick discs 
		stash -= discs
		print("Frolfer " , id ," got " , discs ," discs; Stash = ", stash)
		stash_access.release() #allow other frolfers to access stash
		for b in range(1,discs): #frolfers throwing
			disc_growth.acquire() #frolfer id is throwing
			print("Frolfer ", id , " threw disc ", b )
			discs_on_field += 1
			disc_growth.release() #frolfer id completed throwing. next frolfer can throw now
			time.sleep(rng.random())

def cart():
	global stash
	global discs_on_field
	while True:
		cart_collect.acquire() #wait for cart_collect.release()
		print("Cart entering field")
		disc_growth.acquire() #no more discs can be thrown
		tmp = discs_on_field
		stash += discs_on_field #collect discs from field
		if(stash < 5):
		  print('insufficient discs in field')
		  disc_growth.release()
		  time.sleep(rng.random())
		  disc_growth.acquire()
		  tmp1 = discs_on_field
		  stash+= discs_on_field
		discs_on_field = 0 #all discs collected by cart
		time.sleep(rng.random())
		disc_growth.release() #frolfers can start throwing discs
		print("Cart done, gathered ", tmp," balls; Stash = ", stash)
		stash_full.release() #frolfers can start picking from stash now

if __name__ == '__main__':
	num_frolfers = 0 
	bucketsize =0 #number of discs per frolfer
	stash =0
	#get input from system - number of frolfers, size of bucket,size of stash
	num_frolfers = int(sys.argv[1])
	bucketsize = int(sys.argv[2])
	stash = int(sys.argv[3])
	
	#start the cart and frolfer threads
	ct = Thread(target=cart)
	ct.start()
	for i in range(1,num_frolfers):
		t = Thread(target=frolfer, args=[bucketsize,i])
		t.start()