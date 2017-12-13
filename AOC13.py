from time import time
from collections import defaultdict
from math import gcd


def create_possible_values(cycle, count):
    # If no previous cases have yielded any result, it can be any number up to cycle (2(i-1))
        if len(count) == 0:
            counter = list(range(cycle))

        # However, if there were previous results saved in count
        else:
            yes = [[] for q in range(len(count))]
            c = 0
            for j in count:

                # This section is hard to explain, so here is an example. Say [0, 3] is in count and we are looking at
                # i = 7. Then 0 + 0, 0 + 3, 0 + 6, 0 + 9, ... 0 + 36 all mod 12 will be in a sublist of yes
                # or [0, 3, 6, 9]
                # it creates the values possible based on the values we already know true
                if gcd(cycle, j[1]) != 1:
                    for k in range(cycle * j[1]):  # This loop isn't fully efficient I think, count be narrowed down
                        yes[c].append((j[0]  +  k * j[1])  %  cycle)
                    yes[c] = list(set(yes[c]))

                # if they are relatively prime then all values will show up
                # due to group cyclic generators of Zn or something
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
with open('AOC13Input', 'r') as file:
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
# However, we can derive more by using previous truths

# The results will be saved in count, with each entry looking like [values delay must be, mod n]
count = []

for i in range(longest_firewall + 1):
    if i in data:
        cycle = 2 * (i - 1)
        # First we create the possible mod 2*(k-1) values delay can be based on previous cases
        count_one_cycle = create_possible_values(cycle, count)

        # Now we use the values for which any position have the same firewall length
        # I mentioned earlier that delay != -n mod 2*(k-1), so we test that and remove any -n's from our list
        for j in data[i]:
            if (0-j) % cycle in count_one_cycle:
                count_one_cycle.pop(count_one_cycle.index((0-j) % cycle))

        # Now, only if we only have 1 mod value left, we keep it. Could probably keep them all, but that would take
        # more generalizing. And it's 2am and I don't have time
        if len(count_one_cycle) == 1:
            count.append([count_one_cycle[0], cycle])

print('Mod Formulas True for Delay: ' + str(count))
print('In the form of   delay % x[1] = x[0]')

# Now we want to find the first and second value for which all our mod arithmetic equation hold true
# We will store them in coolnum, because they're cool
coolnum = []
[init, jum] = count.pop()
c = init
while len(coolnum) < 2:
    yes = True
    for x in count:
        if c % x[1] != x[0]:
            yes = False
            break
    if yes:
        coolnum.append(c)
        c *= 2
        # We can jump ahead by a factor of two, since 0-c weren't solutions
        # This next line just makes sure we are still satisfying the final condition
        c -= (c % jum) - init + jum
    c += jum

# Now every solution to the mod formulas will be evenly spaced for reasons, so we start at the first and
# jump by the distance between them every time
delay = coolnum[0]
jump = coolnum[1]-coolnum[0]
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
