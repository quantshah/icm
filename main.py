import os
import sys

# Imports
import numpy as np
from qutip import QubitCircuit
from qutip.qip.icm import *
from geometry.generate import convert
import json

def read_file(filename):
	"""
	Read a file and make a list with gate name, arguments, targets and control bits
	"""
	with open(filename) as f:
		contents = f.readlines()
		contents = [x.strip() for x in contents]

	gate_list = [item.split(" ") for item in contents]
	return gate_list

def get_qubits(contents):
	"""
	Get the number of qubits in the circuit.
	"""
	flat_list = [item for sublist in contents for item in sublist]
	qubits = []
	for item in flat_list:
		try:
			qubits += [int(item)]
		except:
			pass
	return max(qubits) + 1

def make_circuit(gate_list):
	"""
	Make a QubitCircuit from the text file.
	"""
	N = get_qubits(gate_list)
	qcircuit = QubitCircuit(N, reverse_states=False)

	for gate in gate_list:
		if gate[0] == "CNOT":
			target = int(gate[1])
			control = int(gate[2])
			qcircuit.add_gate("CNOT", targets=[target], controls=[control])

		if gate[0] == "SNOT":
			qcircuit.add_gate("SNOT", targets=[int(gate[1])])
		if gate[0] == "TOFFOLI":
			qcircuit.add_gate("TOFFOLI", targets=[int(gate[1])], controls=[int(gate[2]), int(gate[3])])

		if gate[0] == "RX":
			arg_label = None
			arg_value = None
			if gate[2] == "pi/2":
				arg_label = r"\pi/2"
				arg_value = np.pi /2
			else:
				raise("Currently only RX pi/2 is supported")

			qcircuit.add_gate("RX", targets=[int(gate[1])], arg_value = arg_value, arg_label = arg_label)

		if gate[0] == "RZ":
			arg_label = None
			arg_value = None
			if gate[2] == "pi/2":
				arg_label = r"\pi/2"
				arg_value = np.pi /2

			elif gate[2] == "pi/4":
				arg_label = r"\pi/2"
				arg_value = np.pi /2
			else:
				raise("Only RZ pi/2 and pi/4 are supported currently")

			qcircuit.add_gate("RZ", targets=[int(gate[1])], arg_value = arg_value, arg_label = arg_label)

	return (qcircuit)

def make_icm(qcircuit):
	"""
	Make an ICM circuit
	"""
	model = Icm(qcircuit)
	cicm = model.to_icm()
	icm_representation, json_dict = visualise(cicm)

	return (icm_representation, json_dict)

raw_gates = read_file('test.txt')
circuit = make_circuit(raw_gates)

if len(sys.argv) > 1 and sys.argv[1] == "latex":
	try:
		circuit.png
		os.rename("qcirc.png", "outputs/images/circuit.png")
		os.rename("qcirc.pdf", "outputs/pdf/circuit.pdf")
		os.rename("qcirc.tex", "outputs/tex/circuit.tex")
	except:
		print("Latex not setup. Please install latex")

icm_circuit, icm_dict = make_icm(circuit)

json_object = {"format": "icm", "circuit": icm_dict}

convert(json_object)

if len(sys.argv) > 1 and sys.argv[1] == "latex":
	try:
		icm_circuit.png
		os.rename("qcirc.png", "outputs/images/icm.png")
		os.rename("qcirc.pdf", "outputs/pdf/icm.pdf")
		os.rename("qcirc.tex", "outputs/tex/icm.tex")
	except:
		print("Latex not setup. Please install latex")

with open("outputs/circuit.json", 'w') as outfile:
    json.dump(json_object, outfile, sort_keys = False, indent=4)
