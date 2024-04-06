import matplotlib.pyplot as plt
import math, time, cpuinfo
import random

last  = 4294967295     # 4294967295 is the limit for unsigned 32bit
found = 4              # we start from 11, know 2, 3, 5, 7
primes = [3, 5, 7]     # exclude 2 since we only test odd numbers
frequency = [0] * 8000 # should be fine for 100 or gaps of 2000

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
# freqyency[1] = 1    # gap of 4 between 7 and 11
last_prime = 7
for number in range(9, last, 2):
  if is_prime_fast(number):
    gap = number - last_prime
    location = int(gap/2 - 1)
    frequency[location] += 1
    found += 1
    last_prime = number
    if (time.perf_counter_ns() - dot) > 2000000000:
        print(".", end="")
        dot = time.perf_counter_ns()
        column += 1
        if column > 30:
            t = elapsed_time((time.perf_counter_ns() - start)/1000000000)
            print(f" {t} - {number} {int(number*100/last)}% ")
            column = 1
if column > 0:
    print(" ")
duration = (time.perf_counter_ns() - start)/1000000000
print(f"This took: {duration:.9f} seconds. {elapsed_time(duration)}")
print(f"I found {found} prime numbers.")

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
