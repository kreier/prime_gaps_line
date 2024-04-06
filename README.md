# Prime Gaps Line

Create a logarithmic plot of the frequency of gaps between primes up to an arbitrary number.

This was inspired by the the video of Stand-up Maths:

https://youtu.be/SMsTXQYgbiQ

For the log line he calculated the gaps for the first 150,000,000 primes (minute 18:40) This should be able to calcutate within 300 seconds in Python according to my graph https://github.com/kreier/prime

Based on an article by Kerry D. Wong from 2009: 

http://www.kerrywong.com/2009/09/06/an-alternative-illustration-of-prime-number-distribution/

## Graph up to 1 million

![graph to 1 million](docs/graph_1million.png)

This was created in a Jupyter Notebook in 1.5 seconds with the following code:

``` py
import matplotlib.pyplot as plt
import math, time, cpuinfo
import random

last  = 1000000        # 4294967295 is the limit for unsigned 32bit, 2147483647
found = 4              # we start from 11, know 2, 3, 5, 7
primes = [3, 5, 7]     # exclude 2 since we only test odd numbers
frequency = [0] * 100  # should be fine for 100 or gaps of 200

def is_prime(number):
    flag_prime = 1
    for divider in range(3, int(math.sqrt(number)) + 1, 2):
        if number % divider == 0:
            flag_prime = 0
            break
    return flag_prime

def find_primes(largest):
    global primes, found
    for number in range(11, largest + 1, 2):
        if is_prime(number) > 0:
            found += 1
            primes.append(number)

def is_prime_fast(number):
    flag_prime = True
    largest_divider = int(math.sqrt(number)) + 1
    for divider in primes:
        if number % divider == 0:
            flag_prime = False
            break
        if divider > largest_divider:
            break
    return flag_prime

def elapsed_time(seconds):
    hours = int(seconds/3600)
    minutes = int(seconds/60 - hours*60)
    sec = int(seconds - minutes*60 - hours*3600)
    return(f"{hours}h {minutes}min {sec}s")

print(f"Calculating prime numbers to {last} in Python with algorithm v5.4.2024")
print(f"Running on a {cpuinfo.get_cpu_info()['brand_raw']}")
start = time.perf_counter_ns()
dot = start
column = 0    
largest_divider = int(math.sqrt(last))
if largest_divider % 2 == 0:
    largest_divider += 1
print(f'First find prime divisors up to {largest_divider}.')
find_primes(largest_divider)
print(f'Found {found} primes, now use them als divisors.')
frequency[0] = 1    # gap of 2 between 5 and 7
last_prime = 7
for number in range(9, last, 2):
  if is_prime_fast(number):
    gap = number - last_prime
    location = int(gap/2 - 1)
    frequency[location] += 1
    found += 1
    last_prime = number
duration = (time.perf_counter_ns() - start)/1000000000
print(f"This took: {duration:.9f} seconds. {elapsed_time(duration)}")
print(f"I found {found} prime numbers. Should be 78498.")

for i in range(len(frequency) - 1, 1, -1):
  if frequency[i] > 0:
    highest = i
    break

frequency = frequency[0:highest]
plt.plot(frequency)
plt.show()

gapsize = []

for i in range(highest):
  gapsize.append(int((i+1)*2))

plt.scatter(gapsize, frequency)
plt.yscale('log')
plt.show()
```

## Compare graph to 1 million and 100 million

<img src="docs/graph_1million.png" width="49%"> <img src="docs/graph_100million.png" width="49%">
