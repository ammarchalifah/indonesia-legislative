import re


class Factory :
	@staticmethod
	def get_patterns() :
		return [
			UndangUndangRegexPattern(),
			PeraturanPresidenRegexPattern(),
			PeraturanPemerintahRegexPattern()
		]

class Rule :
	def __init__(self) :
		pass

class UndangUndang(Rule) :
	def __init__(self, match) :
		self.tahun = int(match.group(5))
		self.nomor = int(match.group(3))

	def __str__(self) :
		return f"Undang-Undang Nomor {self.nomor} Tahun {self.tahun}"


	def __repr__(self) :
		return self.__str__()

class PeraturanPemerintah(Rule) :
	def __init__(self, match) :
		self.nomor = int(match.group(3))
		self.tahun = int(match.group(5))

	def __str__(self) :
		return f"Peraturan Pemerintah Nomor {self.nomor} Tahun {self.tahun}"

	def __repr__(self) :
		return self.__str__()

class PeraturanPresiden(Rule) :
	def __init__(self, match) :
		self.nomor = int(match.group(3))
		self.tahun = int(match.group(5))

	def __str__(self) :
		return f"Peraturan Presiden Nomor {self.nomor} Tahun {self.tahun}"

	def __repr__(self) :
		return self.__str__()

class RegexPattern :
	def __init__(self) :
		self.pattern = self.get_pattern()

		'''Must be Rule or its children'''
		self.rule_class = self.get_rule_class()

	'''
	Get Rule objects from text
	'''
	def get(self, text) :
		return (self.rule_class(match) for match in re.finditer(self.pattern, text))


class PeraturanPemerintahRegexPattern(RegexPattern) :
	def get_pattern(self) :
		return r"(Peraturan Pemerintah)\s+(Nomor)\s+(\b\d+)\s+(Tahun)\s+(\b\d+)"

	def get_rule_class(self) :
		return PeraturanPemerintah

class PeraturanPresidenRegexPattern(RegexPattern) :
	def get_pattern(self) :
		return r"(Peraturan Presiden)\s+(Nomor)\s+(\b\d+)\s+(Tahun)\s+(\b\d+)"

	def get_rule_class(self) :
		return PeraturanPresiden

class UndangUndangRegexPattern(RegexPattern) :
	def get_pattern(self) :
		return r"(Undang-Undang)\s+(Nomor)\s+(\b\d+)\s+(Tahun)\s+(\b\d+)"

	def get_rule_class(self) :
		return UndangUndang



