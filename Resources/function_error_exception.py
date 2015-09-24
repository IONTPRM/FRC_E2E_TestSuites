class FunctionErrorException(Exception):
	def __init__(self, function_name, error_code, error_msg):
		super(FunctionErrorException, self).__init__(self._getExceptionMsg(function_name, error_code, error_msg))

		self.error_code = error_code
		self.error_msg = error_msg

	def _getExceptionMsg(self, function_name, error_code, error_msg):
		return 'Error executing function{%s} ret_code{%s} Msg{%s}' % (function_name, error_code, error_msg)
