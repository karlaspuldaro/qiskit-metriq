#TODO: Move qasm code to its own file and load it here

qasm_in = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
cx q[3],q[0];
cx q[1],q[0];
cx q[5],q[0];
x q[2];
cx q[2],q[0];
x q[4];
cx q[4],q[0];
"""

import os
from pyzx import routing
from qiskit import qiskit
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.transpiler import CouplingMap, TranspilerError

SAMPLE_SIZE = 100
ARCHITECTURES = ['ibm_rochester', 'rigetti_16q_aspen']

def average(lst):
    return sum(lst) / len(lst)

def run_task(output_file_name: str):
  circuit = QuantumCircuit.from_qasm_str(qasm_in)
  circuit_depth = []
  gate_count = []
  path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "results", output_file_name))
  output_file = open(path, "w")
  print(f"Qiskit version: {qiskit.__version__}", file=output_file)
  print(f"Sample size: {SAMPLE_SIZE}\n", file=output_file)

  # transpile for each architecture using pyzx
  for arch in ARCHITECTURES:
    architecture = routing.create_architecture(arch)
    coupling_map = CouplingMap(architecture.graph.edges())
    print(f"Architecture: {architecture.name}", file=output_file)

    for i in range(SAMPLE_SIZE):
        # transpile
        result = None
        while result is None:
            try:
                result = transpile(circuit, coupling_map=coupling_map, optimization_level=3,
                                   seed_transpiler=i)
                # print('seed_transpiler: ', i)
            except TranspilerError:
                # TODO: save seed value 
                i += SAMPLE_SIZE
        circuit_depth.append(result.depth())
        gate_count.append(sum(result.count_ops().values()))

      # Uncomment the line below to see individual run outputs
      # print("Sample", i+1, "- Circuit depth:", result.depth(), "| Gate count:", sum(result.count_ops().values()))
    
    # Write to file
    output = "Circuit depth ave:" + str(average(circuit_depth)) + "| Gate count ave:" + str(average(gate_count)) + "\n"
    print(f"{output}", file=output_file)

    circuit_depth.clear()
    gate_count.clear()
  
  output_file.close()

# TODO Update the output file format to what is expected from metriq API
run_task(f"{qiskit.__version__}.txt")


'''
# TODO: Investigate errors using qiskit versions below:

0.13.0,
0.14.2:

AttributeError: module 'numpy' has no attribute 'float'.
`np.float` was a deprecated alias for the builtin `float`. To avoid this error in existing code, use `float` by itself. Doing this will not modify any behavior and is safe. If you specifically wanted the numpy scalar type, use `np.float64` here.
The aliases was originally deprecated in NumPy 1.20; for more details and guidance see the original release note at:
    https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations

----
0.15.2:

AttributeError: module 'numpy' has no attribute 'int'.
`np.int` was a deprecated alias for the builtin `int`. To avoid this error in existing code, use `int` by itself. Doing this will not modify any behavior and is safe. When replacing `np.int`, you may wish to use e.g. `np.int64` or `np.int32` to specify the precision. If you wish to review your current use, check the release note link for additional information.
The aliases was originally deprecated in NumPy 1.20; for more details and guidance see the original release note at:
    https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations

'''
