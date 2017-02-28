#Final commit
#3_philosophers.py - MP3 -Assignment 3
#This program was run using Python 3.4 and executed using command prompt
#Sample output
#=============
#Running dining philosophers simulation:5philosophers ,10 meals each
#1.Footman solution,time elapsed: Time:9.314s
#2.Lefthanded solution,time elapsed: Time:5.108s
#3.Tanenbaum solution,time elapsed: Time:5.108s


from threading import Semaphore,Lock,Thread
from time import sleep
from random import random
from timeit import Timer
import random
import sys

(thinking,eating)=(0,1)  #states of philosopher

#returns the id of the left fork
def left_fork(pid):
 return pid

#returns the id of the right fork
def right_fork(pid):
  return (pid + 1)% number_philosophers
  
def right_philosopher(pid): #get the id of the right philosopher
 return (pid + 1)% number_philosophers

def left_philosopher(pid): #get the id of the left philosopher
 return (pid + number_philosophers-1) % number_philosophers
 
#philosopher is hungry and needs forks to eat
def get_fork(pid):
 global mutex 
 global tstate
 
 mutex.acquire()
 tstate[pid]='hungry' 
 test(pid) #test to see if neighours are eating
 mutex.release()

#philosopher has completed eating & goes back to thinking 
def put_fork(pid):
 global mutex
 global tstate
 
 mutex.acquire()
 tstate[pid]='thinking'
 test(right_philosopher(pid)) #check to see if right neighour is hungry
 test(left_philosopher(pid)) #check to see if left neighour is hungry
 mutex.release()
 
def test(pid):
 global tstate
 
 if tstate[pid]=='hungry' and tstate[left_philosopher(pid)]!='eating' and tstate[right_philosopher(pid)]!='eating':
  tstate[pid]='eating'

#In footman solution the footman semaphore limits the number of philosophers who can be at the table at one time to 4  
def footman_solution(pid,meals):
    global fork
    global footman
    state = thinking
    rng = random.Random()
    rng.seed(100)	
	
    for i in range(meals):
        sleep(rng.random())
        if(state == thinking):  #if state is THINKING then check forks and EAT
            footman.acquire()
            fork[right_fork(pid)].acquire()
            fork[left_fork(pid)].acquire()
            state = eating
        else:    # EATING is completed, put down the forks
            fork[right_fork(pid)].release()
            fork[left_fork(pid)].release()
            state = thinking
            footman.release()
    
#In lefthanded solution philosopher2 is assumed to be a leftie and the rest righties. This increases concurrency	
def lefthanded_solution(pid,meals):
    global fork
    state = thinking
    rng = random.Random()
    rng.seed(100)
    for i in range(meals):
        sleep(rng.random())
        if(state == thinking):
		    #Assume any philosopher is a leftie. Here we have chosen philosopher 2
            if(pid == 2):  #philosopher2 is a leftie
                fork[left_fork(pid)].acquire()
                fork[right_fork(pid)].acquire()
                state = eating
            else:  #rightie
                fork[right_fork(pid)].acquire()
                fork[left_fork(pid)].acquire()
                state = eating
        else: #if philosopher is not thinking, but eating
            if(pid == 2):
                fork[left_fork(pid)].release()
                fork[right_fork(pid)].release()
                state == thinking   
            else:
                fork[right_fork(pid)].release()
                fork[left_fork(pid)].release()
                state == thinking
     

def Tanenbaum_solution(pid,meals):
    rng = random.Random()
    rng.seed(100)
    for i in range(meals):
        get_fork(pid)       #signal hungry and get forks
        sleep(rng.random()) #eat for some time
        put_fork(pid)       #complete eating, go back to thinking
	
def run_Footman():
 global number_philosophers
 global number_meals

 phil = [Thread(target=footman_solution, args=[i,number_meals]) for i in range(number_philosophers)]
 for t in phil:t.start()
 for t in phil:t.join()
 
def run_lefthanded():
 global number_philosophers
 global number_meals

 phil1 = [Thread(target=lefthanded_solution, args=[i,number_meals]) for i in range(number_philosophers)]
 for t in phil1:t.start()
 for t in phil1:t.join()
	
def run_Tanenbaum():
 global number_philosophers
 global number_meals

 phil2 = [Thread(target=lefthanded_solution, args=[i,number_meals]) for i in range(number_philosophers)]
 for t in phil2:t.start()
 for t in phil2:t.join()
  
if __name__ == '__main__':
 
 number_philosophers=0
 number_meals=0
 
 number_philosophers = int(sys.argv[1])
 number_meals = int(sys.argv[2])
 
 fork = [Semaphore(1) for i in range(number_philosophers)] #forks same as number of philosophers
 footman = Semaphore(4) #for Footman solution
 mutex = Semaphore(1)
 
 tstate = ['thinking'] * number_philosophers #initial state of all philosophers is thinking
 
 print("Running dining philosophers simulation:" + str(number_philosophers) +"philosophers ," + str(number_meals) + " meals each")
 
 run_Footman()
 timer = Timer(run_Footman)
 print("1.Footman solution,time elapsed:  " + "Time:{:0.3f}s".format(timer. timeit(100)/100))
  
 run_lefthanded()
 timer = Timer(run_lefthanded)
 print("2.Lefthanded solution,time elapsed:  " + "Time:{:0.3f}s".format(timer. timeit(100)/100))
 
 run_Tanenbaum()
 timer = Timer(run_Tanenbaum)
 print("3.Tanenbaum solution,time elapsed:  " + "Time:{:0.3f}s".format(timer. timeit(100)/100))