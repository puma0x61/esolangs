#!/usr/bin/env python3
import sys

def parse(s):
	st = [[]]
	op = []
	for c in s:
		if c == "[":
			st.append([])
			op.append("[")
		elif c == "]":
			x = st.pop()
			if not st or op.pop() != "[":
				raise SyntaxError("unbalanced brackets")
			st[-1].append(("[", x))
		elif c == "{":
			st.append([])
			op.append("{")
		elif c == "}":
			x = st.pop()
			if not st or op.pop() != "{":
				raise SyntaxError("unbalanced brackets")
			st[-1].append(("{", x))
		elif c in "<>^v!":
			st[-1].append(c)
		elif c in "#$,'\"":
			st[-1].append([c, None, None])
		elif c == "@":
			if st[-1] and \
			   isinstance(st[-1][-1], list) and \
			   st[-1][-1][1] is None and \
			   st[-1][-1][2] is None:
				st[-1][-1][1] = c
			else:
				raise SyntaxError("unexpected %c" % c)
		elif c in "&.;:":
			if st[-1] and \
			   isinstance(st[-1][-1], list) and \
			   st[-1][-1][2] is None:
				st[-1][-1][2] = c
			else:
				raise SyntaxError("unexpected %c" % c)
	x = st.pop()
	if st:
		raise SyntaxError("unbalanced brackets")
	return x

class Staeck:
	def __init__(self, input):
		self.stack = []
		self.input = input
		self.sp = 0
		self.ip = 0
		self.outqueue = []
		self.inqueue = []
	def read(self):
		if not self.inqueue:
			c = sys.stdin.read(1)
			if not c:
				return None
			c = ord(c)
			for i in range(8):
				self.inqueue.append((c >> i) & 1)
		return self.inqueue.pop(0)
	def write(self, n):
		self.outqueue.append(n)
		if len(self.outqueue) == 8:
			c = 0
			for i, x in enumerate(self.outqueue):
				c |= x << i
			sys.stdout.write(chr(c))
			self.outqueue = []
	def run(self, ast):
		for x in ast:
			if isinstance(x, list):
				if x[0] == "#":
					if not self.input:
						return False
					n = self.input[self.ip]
				elif x[0] == "$":
					if not self.stack:
						return False
					n = self.stack[self.sp]
				elif x[0] == ",":
					n = self.read()
					if n is None:
						return False
				elif x[0] == "'":
					n = 0
				elif x[0] == "\"":
					n = 1
				if x[1] == "@":
					n ^= 1
				if x[2] == "&":
					self.stack.append(n)
				elif x[2] == ".":
					self.write(n)
				elif x[2] == ";":
					if n == 0:
						return False
				elif x[2] == ":":
					if n == 1:
						return False
			elif isinstance(x, tuple):
				if x[0] == "[":
					self.run(x[1])
				elif x[0] == "{":
					while self.run(x[1]):
						pass
			elif x == "<":
				if not self.input or \
				   self.ip == 0:
					return False
				self.ip -= 1
			elif x == ">":
				if not self.input or \
				   self.ip == len(self.input) - 1:
					return False
				self.ip += 1
			elif x == "^":
				if not self.stack or \
				   self.sp == len(self.stack) - 1:
					return False
				self.sp += 1
			elif x == "v":
				if not self.stack or \
				   self.sp == 0:
					return False
				self.sp -= 1
			elif x == "!":
				return False
		return True

if __name__ == "__main__":
	if len(sys.argv) < 3 or \
	   len(sys.argv) > 4 or \
	   (len(sys.argv) == 4 and sys.argv[1] != "-f"):
		print("Usage: %s [-f] CODE INPUT" % sys.argv[0], file=sys.stderr)
		exit(1)
	if sys.argv[1] == "-f":
		with open(sys.argv[2]) as f:
			code = f.read()
		inp = sys.argv[3]
	else:
		code = sys.argv[1]
		inp = sys.argv[2]
	inp = list(map(lambda x: int(x) % 2, inp))
	st = Staeck(inp)
	r = st.run(parse(code))
	if r:
		exit(0)
	exit(1)

