class PlatformEnumBase:
	def __init__(self, string_to_code_dictionary):
		self.string_to_code = string_to_code_dictionary

		strings = self.string_to_code.keys()
		self._validate_strings_are_strings(strings)

		codes = self.string_to_code.values()
		self.validate_codes(codes)

		self.code_to_string = dict(zip(codes, strings))
		lower_case_strings = map(lambda string: string.lower(), strings)
		self.lower_case_to_string = dict(zip(lower_case_strings, strings))

	def _validate_strings_are_strings(self, strings):
		for string in strings:
			if not isinstance(string, str):
				raise ValueError('Keys must all be strings')

	def get_string(self, string_or_code):
		return self._get_string(string_or_code)

	def _get_string(self, string_or_code, try_code=True):
		if string_or_code in self.string_to_code:
			return string_or_code
		string = str(string_or_code).lower()
		if string in self.lower_case_to_string:
			return self.lower_case_to_string[string]
		if try_code:
			return self.code_to_string[self._get_code(string_or_code, False)]
		raise ValueError('Invalid Platform Enum Value ' + string)

	def get_code(self, string_or_code):
		return self._get_code(string_or_code)

	def _get_code(self, string_or_code, try_string=True):
		if string_or_code in self.code_to_string:
			return string_or_code
		code = self.parse_code(string_or_code)
		if code != None:
			return code
		if try_string:
			return self.string_to_code[self._get_string(string_or_code, False)]
		raise ValueError('Invalid Platform Enum Value ' + str(string_or_code))

class PlatformEnum(PlatformEnumBase):
	def __init__(self, string_to_code_dictionary):
		PlatformEnumBase.__init__(self, string_to_code_dictionary)

	def validate_codes(self, codes):
		for code in codes:
			if not isinstance(code, int):
				raise ValueError('Codes must all be integers')

	def parse_code(self, string_or_code):
		try:
			code = int(string_or_code)
			if code in self.code_to_string:
				return code
		except:
			return None

class PlatformStringEnum(PlatformEnumBase):
	def __init__(self, string_to_code_dictionary):
		PlatformEnumBase.__init__(self, string_to_code_dictionary)
		codes = self.string_to_code.values()
		lower_case_codes = map(lambda code: code.lower(), codes)
		self.lower_case_to_code = dict(zip(lower_case_codes, codes))

	def validate_codes(self, codes):
		for code in codes:
			if not isinstance(code, str):
				raise ValueError('Codes must all be strings')

	def parse_code(self, string_or_code):
		lower_case_code = str(string_or_code).lower()
		if lower_case_code in self.lower_case_to_code:
			return self.lower_case_to_code[lower_case_code]
		return None

import unittest
class TestPlatformEnum(unittest.TestCase):
	def setUp(self):
		self.enum = PlatformEnum({'Yes' : 1, 'No' : 2})

	def test_constructor_string_value_error(self):
		invalid_dictionary = {'Yes' : 1, 2 : 2}
		self.assertRaises(ValueError, PlatformEnum, invalid_dictionary)

	def test_constructor_code_value_error(self):
		invalid_dictionary = {'Yes' : 1, 'No' : '2'}
		self.assertRaises(ValueError, PlatformEnum, invalid_dictionary)

	def test_get_code_1_success_cases(self):
		expected_value = 1
		self.assertEqual(self.enum.get_code('YES'), expected_value)
		self.assertEqual(self.enum.get_code('YEs'), expected_value)
		self.assertEqual(self.enum.get_code('YeS'), expected_value)
		self.assertEqual(self.enum.get_code('Yes'), expected_value)
		self.assertEqual(self.enum.get_code('yeS'), expected_value)
		self.assertEqual(self.enum.get_code('yes'), expected_value)
		self.assertEqual(self.enum.get_code('YeS'), expected_value)
		self.assertEqual(self.enum.get_code('Yes'), expected_value)
		self.assertEqual(self.enum.get_code(1), expected_value)
		self.assertEqual(self.enum.get_code('1'), expected_value)

	def test_get_code_2_success_cases(self):
		expected_value = 2
		self.assertEqual(self.enum.get_code('NO'), expected_value)
		self.assertEqual(self.enum.get_code('No'), expected_value)
		self.assertEqual(self.enum.get_code('nO'), expected_value)
		self.assertEqual(self.enum.get_code('no'), expected_value)
		self.assertEqual(self.enum.get_code(2), expected_value)
		self.assertEqual(self.enum.get_code('2'), expected_value)

	def test_get_string_1_success_cases(self):
		expected_value = 'Yes'
		self.assertEqual(self.enum.get_string('YES'), expected_value)
		self.assertEqual(self.enum.get_string('YEs'), expected_value)
		self.assertEqual(self.enum.get_string('YeS'), expected_value)
		self.assertEqual(self.enum.get_string('Yes'), expected_value)
		self.assertEqual(self.enum.get_string('yeS'), expected_value)
		self.assertEqual(self.enum.get_string('yes'), expected_value)
		self.assertEqual(self.enum.get_string('YeS'), expected_value)
		self.assertEqual(self.enum.get_string('Yes'), expected_value)
		self.assertEqual(self.enum.get_string(1), expected_value)
		self.assertEqual(self.enum.get_string('1'), expected_value)

	def test_get_string_2_success_cases(self):
		expected_value = 'No'
		self.assertEqual(self.enum.get_string('NO'), expected_value)
		self.assertEqual(self.enum.get_string('No'), expected_value)
		self.assertEqual(self.enum.get_string('nO'), expected_value)
		self.assertEqual(self.enum.get_string('no'), expected_value)
		self.assertEqual(self.enum.get_string(2), expected_value)
		self.assertEqual(self.enum.get_string('2'), expected_value)

	def test_get_code_error_cases(self):
		self.assertRaises(ValueError, self.enum.get_code, 3)
		self.assertRaises(ValueError, self.enum.get_code, '3')
		self.assertRaises(ValueError, self.enum.get_code, 'OtherString')

	def test_get_string_error_cases(self):
		self.assertRaises(ValueError, self.enum.get_string, 3)
		self.assertRaises(ValueError, self.enum.get_string, '3')
		self.assertRaises(ValueError, self.enum.get_string, 'OtherString')

class TestPlatformStringEnum(unittest.TestCase):
	def setUp(self):
		self.enum = PlatformStringEnum({'Yes' : 'Y', 'No' : 'N'})

	def test_constructor_string_value_error(self):
		invalid_dictionary = {'Yes' : 1, 2 : 2}
		self.assertRaises(ValueError, PlatformStringEnum, invalid_dictionary)

	def test_constructor_code_value_error(self):
		invalid_dictionary = {'Yes' : 1, 'No' : '2'}
		self.assertRaises(ValueError, PlatformStringEnum, invalid_dictionary)

	def test_get_code_Y_success_cases(self):
		expected_value = 'Y'
		self.assertEqual(self.enum.get_code('YES'), expected_value)
		self.assertEqual(self.enum.get_code('YEs'), expected_value)
		self.assertEqual(self.enum.get_code('YeS'), expected_value)
		self.assertEqual(self.enum.get_code('Yes'), expected_value)
		self.assertEqual(self.enum.get_code('yeS'), expected_value)
		self.assertEqual(self.enum.get_code('yes'), expected_value)
		self.assertEqual(self.enum.get_code('YeS'), expected_value)
		self.assertEqual(self.enum.get_code('Yes'), expected_value)
		self.assertEqual(self.enum.get_code('Y'), expected_value)
		self.assertEqual(self.enum.get_code('y'), expected_value)

	def test_get_code_N_success_cases(self):
		expected_value = 'N'
		self.assertEqual(self.enum.get_code('NO'), expected_value)
		self.assertEqual(self.enum.get_code('No'), expected_value)
		self.assertEqual(self.enum.get_code('nO'), expected_value)
		self.assertEqual(self.enum.get_code('no'), expected_value)
		self.assertEqual(self.enum.get_code('N'), expected_value)
		self.assertEqual(self.enum.get_code('n'), expected_value)

	def test_get_string_Y_success_cases(self):
		expected_value = 'Yes'
		self.assertEqual(self.enum.get_string('YES'), expected_value)
		self.assertEqual(self.enum.get_string('YEs'), expected_value)
		self.assertEqual(self.enum.get_string('YeS'), expected_value)
		self.assertEqual(self.enum.get_string('Yes'), expected_value)
		self.assertEqual(self.enum.get_string('yeS'), expected_value)
		self.assertEqual(self.enum.get_string('yes'), expected_value)
		self.assertEqual(self.enum.get_string('YeS'), expected_value)
		self.assertEqual(self.enum.get_string('Yes'), expected_value)
		self.assertEqual(self.enum.get_string('Y'), expected_value)
		self.assertEqual(self.enum.get_string('y'), expected_value)

	def test_get_string_N_success_cases(self):
		expected_value = 'No'
		self.assertEqual(self.enum.get_string('NO'), expected_value)
		self.assertEqual(self.enum.get_string('No'), expected_value)
		self.assertEqual(self.enum.get_string('nO'), expected_value)
		self.assertEqual(self.enum.get_string('no'), expected_value)
		self.assertEqual(self.enum.get_string('N'), expected_value)
		self.assertEqual(self.enum.get_string('n'), expected_value)

	def test_get_code_error_cases(self):
		self.assertRaises(ValueError, self.enum.get_code, 3)
		self.assertRaises(ValueError, self.enum.get_code, '3')
		self.assertRaises(ValueError, self.enum.get_code, 'OtherString')

	def test_get_string_error_cases(self):
		self.assertRaises(ValueError, self.enum.get_string, 3)
		self.assertRaises(ValueError, self.enum.get_string, '3')
		self.assertRaises(ValueError, self.enum.get_string, 'OtherString')

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestPlatformEnum)
	unittest.TextTestRunner(verbosity = 2).run(suite)
	suite = unittest.TestLoader().loadTestsFromTestCase(TestPlatformStringEnum)
	unittest.TextTestRunner(verbosity = 2).run(suite)

