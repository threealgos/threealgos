import cirq
from bitcoin import *

# Function to create a quantum circuit for generating random bits
def create_random_bit_circuit(num_bits):
    # Create qubits
    qubits = [cirq.NamedQubit(f"q{i}") for i in range(num_bits)]
    
    # Create a circuit
    circuit = cirq.Circuit()
    
    # Apply Hadamard gate to each qubit to put them in superposition
    circuit.append(cirq.H(q) for q in qubits)
    
    # Measure the qubits
    circuit.append(cirq.measure(*qubits, key='result'))
    
    return circuit

# Function to run the quantum circuit and get a random number
def run_quantum_random_number(num_bits):
    # Create the circuit
    circuit = create_random_bit_circuit(num_bits)
    
    # Create a simulator
    simulator = cirq.Simulator()
    
    # Run the circuit
    result = simulator.run(circuit, repetitions=1)
    
    # Extract the result as a binary string
    random_bits = ''.join(str(result.measurements['result'][0][i]) for i in range(num_bits))
    
    # Convert binary string to an integer
    random_number = int(random_bits, 2)
    return random_number

# Main loop to generate random numbers
while True:
    # Generate a random number using the quantum circuit
    num_bits = 68  # Bitcoin private keys are 68 bits
    random_number = run_quantum_random_number(num_bits)
    
    # Convert the random number to a hexadecimal representation
    hex_value = hex(random_number)[2:].rjust(64, '0')  # 64 hex digits for 256 bits
    
    # Generate the corresponding public address
    priv = hex_value
    pub = privtopub(priv)
    pubkey1 = encode_pubkey(pub, "bin_compressed")
    addr = pubtoaddr(pubkey1)
    
    # Print the generated value
    print("Generated random value:", hex_value)
    
    # Check if the generated address matches the target address
    if addr == '1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ':
        print("Found!!", addr, "with private key:", priv)
        # Save the result to a file
        with open('boom.txt', 'a') as file:
            file.write("Private key: " + priv + '\n' + "Address: " + addr + '\n\n')
        break  # Exit the loop if the condition is met
    else:
        print("Searching...", addr, hex_value, end='\r')