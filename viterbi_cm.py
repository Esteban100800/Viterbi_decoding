import math
import random

# branch outputs: expected coded bits for each branch (same trellis as viterbi.py)
branch_bit = [0b00, 0b11, 0b10, 0b01, 0b11, 0b00, 0b01, 0b10]

# decoded info bit for each branch
branch_bit_decoded = [0, 1, 0, 1, 0, 1, 0, 1]


def create(size):
    return [None] * size


# Step 2: CM branch metric
# BPSK mapping: bit 0 -> +1, bit 1 -> -1
# metric = s1*r1 + s2*r2   (to be MAXIMIZED)
def cm_branch_metric(branch_idx, r1, r2):
    expected = branch_bit[branch_idx]
    c1 = (expected >> 1) & 1
    c2 =  expected       & 1
    s1 = 1 - 2 * c1   # bit 0 -> +1, bit 1 -> -1
    s2 = 1 - 2 * c2
    return s1 * r1 + s2 * r2


# Step 1: initialize — Problem 34-2 received sequence (rate 1/2, 9 pairs)
# Figure trellis example — received pairs (r1, r2) for each t=1..9
# t:  1        2       3        4         5       6       7       8       9
#rcv = [-1,+0.1, -1,+1, -1,+0.1, -0.2,+1, -1,-1, +1,-1, +1,-1, -1,-1, +1,+1]
#rcv = [+1,+1, +0.6,-1, 1,-1, -1,0.1, +1,-1, -1,-1, 0.3,-1, -1,+1, -1,-1]

rcv= [-1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1]
r1_array = rcv[0::2]   # even-indexed: first of each pair
r2_array = rcv[1::2]   # odd-indexed:  second of each pair
n = len(r1_array)

state_matrix  = [[None for _ in range(4)] for _ in range(n + 1)]
branch_matrix = [[None for _ in range(4)] for _ in range(n + 1)]

# initialize: only state '00' (index 0) has metric 0, rest are -inf
state_matrix[0] = [0.0, -math.inf, -math.inf, -math.inf]

print(f"n = {n} symbol pairs")
print(f"r1 samples: {r1_array}")
print(f"r2 samples: {r2_array}")

for i in range(1, n + 1):
    state_matrix[i] = [-math.inf] * 4

# Steps 2-5: forward pass
for i in range(1, n + 1):
    r1 = r1_array[i - 1]
    r2 = r2_array[i - 1]

    # state 0: arrives from state 0 (branch 0) or state 2 (branch 4)
    m0 = state_matrix[i - 1][0] + cm_branch_metric(0, r1, r2)
    m4 = state_matrix[i - 1][2] + cm_branch_metric(4, r1, r2)
    state_matrix[i][0] = max(m0, m4)
    if m0 > m4:
        branch_matrix[i][0] = 0
    elif m4 > m0:
        branch_matrix[i][0] = 4
    else:
        branch_matrix[i][0] = random.choice([0, 4])   # tie-break

    # state 1: arrives from state 0 (branch 1) or state 2 (branch 5)
    m1 = state_matrix[i - 1][0] + cm_branch_metric(1, r1, r2)
    m5 = state_matrix[i - 1][2] + cm_branch_metric(5, r1, r2)
    state_matrix[i][1] = max(m1, m5)
    if m1 > m5:
        branch_matrix[i][1] = 1
    elif m5 > m1:
        branch_matrix[i][1] = 5
    else:
        branch_matrix[i][1] = random.choice([1, 5])   # tie-break

    # state 2: arrives from state 1 (branch 2) or state 3 (branch 6)
    m2 = state_matrix[i - 1][1] + cm_branch_metric(2, r1, r2)
    m6 = state_matrix[i - 1][3] + cm_branch_metric(6, r1, r2)
    state_matrix[i][2] = max(m2, m6)
    if m2 > m6:
        branch_matrix[i][2] = 2
    elif m6 > m2:
        branch_matrix[i][2] = 6
    else:
        branch_matrix[i][2] = random.choice([2, 6])   # tie-break

    # state 3: arrives from state 1 (branch 3) or state 3 (branch 7)
    m3 = state_matrix[i - 1][1] + cm_branch_metric(3, r1, r2)
    m7 = state_matrix[i - 1][3] + cm_branch_metric(7, r1, r2)
    state_matrix[i][3] = max(m3, m7)
    if m3 > m7:
        branch_matrix[i][3] = 3
    elif m7 > m3:
        branch_matrix[i][3] = 7
    else:
        branch_matrix[i][3] = random.choice([3, 7])   # tie-break

    for j in range(4):
        print(f"state_matrix[{i}][{j}] = {state_matrix[i][j]}")

print(f"state matrix:\n{state_matrix}")
print(branch_matrix)



path = [None] * (n + 1)
for j in range(n, -1, -1):
    candidate = state_matrix[j][0]
    path[j] = 0 
    for i in range(4): 
        print(state_matrix[j][i]) 
        if state_matrix[j][i] >= candidate:
            candidate = state_matrix[j][i]
            path[j] = i  

info_bits = []  
for i in range(1, n + 1):
    info_bits.append(branch_bit_decoded[branch_matrix[i][path[i]]]) 
print(info_bits)
