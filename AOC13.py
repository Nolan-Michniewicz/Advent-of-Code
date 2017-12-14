from time import time
from collections import defaultdict
from math import gcd
from functools import reduce

input_file = 'AOC13Input'


def lcm(a, b):
    return a * b // gcd(a, b)


def lcmm(args):
    return reduce(lcm, args)


# Inputs: cycle - a cycle length      
# count - a list that includes previous cycle lengths if they force delay to be one specific modular residue of Z_{Prev_Cycle_Lengths}
#
# Output: a list of possible residues delay can be mod Z_cycle based only upon count

def create_possible_values(cycle, count):
    # If no previous cases have yielded any result, it can be any number up to cycle
        if len(count) == 0:
            counter = list(range(cycle))

        # However, if there were previous results saved in count
        else:
            yes = [[] for q in range(len(count))]   # Creates a list of subslists, one for each member in count
            c = 0   # Counter for which member in count we are using
            for j in count:

                # This section is hard to explain, so here is an example. Assume [2, 6] is in count and we are looking at
                # i = 6. Then 2 + 0, 2 + 6, 2 + 12, 2 + 18, 2 + 24  all mod 10 will be in a sublist of yes
                # or [2, 8, 4, 0, 6]
                # it creates the residues possible based on one residue we already know true
                
                if gcd(cycle, j[1]) != 1:
                    for k in range(int(cycle / gcd(cycle, j[1]))): 
                        yes[c].append((j[0]  +  k * j[1])  %  cycle)

                # if they are relatively prime then all values will show up
                # due to group cyclic generators of Z/nZ
                else:
                    yes[c] = list(range(cycle))
                    
                c += 1

            # Start off counter as all possible values
            counter = set(range(cycle))
            # Now only keeps a value if it is true for all the equations before
            for j in yes:
                counter = counter and set(j)
        return list(counter)

start = time()

# Splits inputs into list lines
lines = []
with open(input_file, 'r') as file:
    for line in file:
        lines.append([int(x) for x in line.replace(':', '').strip().split(' ')])


# PART 1
# ---------------------------------------------------------------------------
total = 0
for line in lines:
    if line[0] % (2 * (line[1] - 1)) == 0:
        total += line[0] * line[1]
print('Part 1: ' + str(total))


# PART 2
# ---------------------------------------------------------------------------


longest_firewall = max([x[1] for x in lines])

# creates a dictionary, data, where the key is a firewall length and
# the value is a list with all positions with that firewall length
data = defaultdict(list)
for i in lines:
    data[i[1]].append(i[0])


# We will now create a list of all the truths we know about the delay
# Start with the lowest firewall length k with position n,
# delay + n != 0 mod 2*(k-1)   OR   delay != -n mod 2*(k-1)
# So from our dictionary, if the key provides a list of length m, we have m of the above equations
# However, we can derive more by using previous firewall lengths

# The results will be saved in count, with each entry looking like [residue delay must be mod n, n]
count = []

for i in range(longest_firewall + 1):
    if i in data:
        cycle = 2 * (i - 1)
        # First we create the possible mod 2*(k-1) values delay can be based on previous cases
        count_one_cycle = create_possible_values(cycle, count)

        # Now we use the values for which any position have the same firewall length
        # I mentioned earlier that delay != -n mod 2*(k-1), so we test that and remove any -n's from our list
        if len(count_one_cycle) > 1:
            for j in data[i]:
                temp = (0-j) % cycle
                if temp in count_one_cycle:
                    count_one_cycle.pop(count_one_cycle.index(temp))

        # Now, only if we only have 1 modular residue left, we keep it. 
        # I tested keeping them all, and it added time, I think the time gain for the small chance
        # of finding another 1 mod value isn't worth it
        if len(count_one_cycle) == 1:
            count.append([count_one_cycle[0], cycle])

print('Mod Formulas True for Delay: ' + str(count))
print('In the form of   delay % x[1] = x[0]')

# Now we want to find the first for which all our mod arithmetic equation hold true
# We will store this in coolnum, because it's cool

# in order to make the next loops faster, we automatically take the biggest cycle length we have
# only one residue for and only test those numbers that make that true
if len(count) > 0:
    [init, jum] = count.pop()
    c = init

    yes = False
    while not yes:
        yes = True
        for x in count:
            if c % x[1] != x[0]:
                yes = False
                break
        if yes:
            coolnum = c
        c += jum

    # Now every solution to the mod formulas will be evenly spaced,
    # with the distance between them being the least common multiple
    # of all the firewall lengths, since that's the first number
    # to maintain all modular residues if added
    count.append([init, jum])
    delay = coolnum
    jump = lcmm([x[1] for x in count])
else:
    delay = 0
    jump = 1

print('First possible delay: ' + str(delay))
print('Jump distance: ' + str(jump))


# Final Part, just tests the long way
cont = True

while cont:
    cont = False
    for x in lines:
        if (x[0] + delay) % (2 * (x[1] - 1)) == 0:
            cont = True
            break
    if not cont:
        print('Part Two: ' + str(delay))
    delay += jump


print('Completed in ' + str(time() - start) + ' seconds.')
