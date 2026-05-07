import math

state_metric = [0.0, math.inf, math.inf, math.inf]


branch = [1, 2, 3, 4, 5, 6 , 7]

branch_bit = [0b00, 0b11, 0b10, 0b01, 0b11, 0b00, 0b01, 0b10]

branch_bit_decoded = [0,1,0,1,0,1,0,1]


# dynamic array
def create(size):
    return [None] * size




# input the k + 2 values of the received bits (k = 7, so k + 2 = 9)
n = int(input("how many bits sent?"))


t_array = create(n)

bit_array = create(n)

state_matrix = [[None for _ in range(4)] for _ in range(n + 1)]
branch_matrix = [[None for _ in range(4)] for _ in range(n + 1)]

# info bits received
print("Please, input the received bits (00, 01, 10 o 11):")
for i in range(n):
    while True:
        bits = input(f"Bits in position {i}: ")
        if bits in ['00', '01', '10', '11']:
            bit_array[i] = int(bits, 2)  # Convierte binar00io a decimal
            break
        else:
            print("Please enter only 00, 01, 10 or 11")

print(f"Bits sent: {bit_array}")

# first row of state_matrix: only state '00' (0) has metric 0, the rest are infinity
state_matrix[0]  = [0.0, math.inf, math.inf, math.inf]


def get_msb(value, bits=2):
    """returns the most significant bit (MSB) of a value given the total number of bits."""
    return (value >> (bits - 1)) & 1

def get_lsb(value):

    return value & 1

def bits_str(value, bits=2):
    """returns a string representation of the bits of a value, padded to the specified number of bits."""
    s = format(value, f'0{bits}b')
    return int(s[0]), int(s[1])



for i in range(1, n + 1):
    state_matrix[i] = [math.inf, math.inf, math.inf, math.inf]



def invert_bit(bit):
    """Inverts a single bit (0 to 1, or 1 to 0)."""
    return bit ^ 1



# branch_metric: calculates the Hamming distance between the expected bits for a branch and the received symbol.
def branch_metric(branch_idx, received):
    """Returns the Hamming distance between the expected bits for a branch and the received symbol."""
    expected = branch_bit[branch_idx]  # 2-bit value for the branch
    return bin(expected ^ received).count('1')


state_matrix


print(f"Bits sent: {bit_array}")

# Determine the number of steps to process
steps = min(n, len(bit_array))
if steps != n:
    print(f"Warning: requested n={n} but only {len(bit_array)} symbols available, using steps={steps}")


for i in range(1, steps + 1):
    received = bit_array[i - 1]

    
    state_matrix[i][0] = min(
        state_matrix[i - 1][0] + branch_metric(0, received),  # branch 1
        state_matrix[i - 1][2] + branch_metric(4, received),  # branch 5
    )

    if state_matrix[i - 1][0] + branch_metric(0, received) <= state_matrix[i - 1][2] + branch_metric(4, received):
        branch_matrix[i][0] = 0  # branch 1
    else:
        branch_matrix[i][0] = 4  # branch 5

    state_matrix[i][1] = min(
        state_matrix[i - 1][0] + branch_metric(1, received),  # branch 2
        state_matrix[i - 1][2] + branch_metric(5, received),  # branch 6
    )


    if state_matrix[i - 1][0] + branch_metric(1, received) <= state_matrix[i - 1][2] + branch_metric(5, received):
        branch_matrix[i][1] = 1  # branch 2
    else:
        branch_matrix[i][1] = 5  # branch 6


    
    state_matrix[i][2] = min(
        state_matrix[i - 1][1] + branch_metric(2, received),  # branch 3
        state_matrix[i - 1][3] + branch_metric(6, received),  # branch 7
    )

    if state_matrix[i - 1][1] + branch_metric(2, received) <= state_matrix[i - 1][3] + branch_metric(6, received):
        branch_matrix[i][2] = 2  # branch 3
    else:
        branch_matrix[i][2] = 6  # branch 7

    state_matrix[i][3] = min(
        state_matrix[i - 1][1] + branch_metric(3, received),  # branch 4
        state_matrix[i - 1][3] + branch_metric(7, received),  # branch 8
    )


    if state_matrix[i - 1][1] + branch_metric(3, received) <= state_matrix[i - 1][3] + branch_metric(7, received):
        branch_matrix[i][3] = 3  # branch 4
    else:
        branch_matrix[i][3] = 7  # branch 8
    for j in range(4):
        print(f"state_matrix[{i}][{j}] = {state_matrix[i][j]}")

print(f"state matrix:\n{state_matrix}")

print (branch_matrix)

path = [None] * (steps + 1)
for j in range(n, -1, -1):
    
    candidate = state_matrix[j][0]
    path[j] = 0 
    for i in range(4): 
        print(state_matrix[j][i]) 
        if state_matrix[j][i] <= candidate:
            candidate = state_matrix[j][i]
            path[j] = i  


for j in range(n, -1, -1):
    print (path[j])



info_bits = []  
for i in range(1, steps + 1):
    info_bits.append(branch_bit_decoded[branch_matrix[i][path[i]]]) 




print (f"Decoded info bits: {info_bits}")


