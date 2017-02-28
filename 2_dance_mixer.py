#Final commit
#Dance mixer problem with 2 leaders and 5 followers
#2_dance_mixer.py - MP3 -Assignment 2
#This program was run using Python 3.4 and was executed using command prompt
#Code present online was referred to for understanding purposes
#Algorithm followed:
#Start off the leader and follower threads 
#what they will do is add to the respective deque and then block on the hand semaphore
#the start music releases the block on hand semaphore enabling the leader and follower to be popped from the deque for dancing
#the dance goes on for 5 seconds, and then the music changes to the next in music_list
#music is stopped and changed only once the leaders and followers have come back in line - a problem with this since even after dancing is over
#a leader goes back into line

import random
import time
from time import sleep
from threading import Thread, Lock, Semaphore
from collections import deque
from itertools import cycle

rng = random.Random()
rng.seed(50)

leaders = deque()  #Queue for leaders
followers = deque() #Queue for followers

leader_queue = Semaphore(1) #Lock on the leader line up for dancing
followers_queue = Semaphore(1) #Lock on the followers line up for dancing

leader_hand = Semaphore(0)
follower_hand = Semaphore(0)

dance_floor = Semaphore(1) #for if dance_floor is empty or not

numleaders = 0  #number of leaders initially 0
numfollowers = 0 #number of followers initially 0

def leader_main(leader_id):
	global leaders
	global followers
	
	leader_queue.acquire()
	leaders.append(leader_id)
	leader_queue.release()
	
	while True:
		leader_enter_floor(leader_id)
		leader_dance(leader_id)
		leader_line_up(leader_id)

def leader_enter_floor(leader_id):
	leader_hand.acquire()
	print('Leader' + str(leader_id) + ' entering floor')
	while len(followers)==0:
		pass
	followers_queue.acquire()
	#get a follower from the deque
	n_follower = followers.popleft()
	followers_queue.release()
	follower_hand.release() #follower ready for dancing
	print('Follower ' + str(n_follower) + ' entering floor')
	print('Leader ' + str(leader_id) + 'and' + 'follower ' + str(n_follower) + ' are dancing')
	
def leader_dance(leader_id):
	dance_floor.acquire()
	sleep(rng.random())
	
def leader_line_up(leader_id):
	leader_queue.acquire()
	leaders.append(leader_id)
	print('Leader ' + str(leader_id) + 'getting back in line')
	leader_queue.release()
	dance_floor.release()
	
def follower_main(follower_id):
	global leaders
	global followers
	
	followers_queue.acquire()
	followers.append(follower_id)
	followers_queue.release()
	
	while True:
		follower_enter_floor(follower_id)
		follower_dance(follower_id)
		follower_line_up(follower_id)

def follower_enter_floor(follower_id):
	follower_hand.acquire()
	
def follower_dance(follower_id):
	dance_floor.acquire()
	sleep(rng.random())
	
def follower_line_up(follower_id):
	followers_queue.acquire()
	followers.append(follower_id) #add back to deque
	print('Follower ' + str(follower_id) + 'getting back in line')
	followers_queue.release()
	dance_floor.release()
	
music_list = ['waltz', 'tango', 'foxtrot']

def startmusic(mus):
	print('*** Band leader started playing ' + mus)
	start = time.time()
	
	while (time.time() - start) < 5:
		if len(leaders) > 0:
			leader_queue.acquire()
			n_leader = leaders.popleft() #pop from leaders deque for dancing
			leader_queue.release()
			leader_hand.release()
	
def endmusic(mus):
		print('*** Band leader stopped playing ' + mus)


if __name__ == '__main__':
	
	#for this assignment we assume 2 leaders and 5 followers
	num_leaders = 2
	num_followers = 5
	
	#start the leaders and followers threads
	for i in range(1,num_leaders):
		t = Thread(target=leader_main, args=[i])
		t.start()
		
	for j in range(1,num_followers):
		t1 = Thread(target=follower_main, args=[j])
		t1.start()
		
	for m in music_list:
		startmusic(m)
		endmusic(m)
	
	print('Dancing over')