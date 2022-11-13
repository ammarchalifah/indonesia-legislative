import argparse
import os
import sys

import patterns

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import document_processor

class Network :
	def __init__(self) :
		self.processor = document_processor.DocumentProcessor()
		self.rules = []
		self.patterns = patterns.Factory.get_patterns()

	# Get all rules network
	def extract_network(self, input) :
		with open(input, "r") as f :
			text = f.read()
			for pattern in self.patterns : 
				self.rules.extend(pattern.get(text))


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()

    network = Network()
    network.extract_network(args.input)

    print(network.rules)