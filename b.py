from a import a

class b(a):
	def __init__(self, name="B"):
		super().__init__(name)

	def b_method(self):
		return f"{self.name} -> method b"