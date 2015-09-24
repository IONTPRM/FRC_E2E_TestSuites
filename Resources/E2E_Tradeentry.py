from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.libraries.Process import Process

from function_error_exception import FunctionErrorException
import E2E_Utility

def execute_te_function(function_name, *fv):
	res= BuiltIn().run_keyword('Exec Function', '${TRADEENTRY SRC}_'+function_name, '${TIMEOUT_MSEC}', *fv)
	return_code, result = res.split(':', 1)
	if (return_code != str(0)):
		raise FunctionErrorException(function_name, return_code, result)
	return result

_te_action_table_prefix = '${TRADEENTRY CURR}.TRADEENTRYACTION.${TRADEENTRY SRC}' 
def get_te_action_record_id(te_action_id):
	return '%s.%s' % (_te_action_table_prefix, te_action_id)
	
def create_manual_trade(instr_id, value, value_type, verbstr, qty):
	"""This keyword creates a single leg trade using tradeentry and returns trade id
	"""
	if verbstr == 'Buy':
		verb = 1
	elif verbstr == 'Sell':
		verb = 2
		
	te_action_id = execute_te_function('CreateTrade')
	transaction_fvs = ('CreateUserId', '${COMMON MKVUSER}', 'InstrumentId', instr_id, 'Value', value, 'ValueType', E2E_Utility.get_value_type_int(value_type), 'Verb', verb, 'Qty', qty, 'BookId', '${BOOKID}', 'RecalcFlag', 1)
	BuiltIn().run_keyword('Exec Transaction', get_te_action_record_id(te_action_id), '${TIMEOUT_MSEC}', *transaction_fvs)

	BuiltIn().run_keyword('Sleep', '1s', 'Just to wait for 1 second in case ticket is not initialized correctly yet')

	transaction_fvs = ('Value', value, 'ValueType', E2E_Utility.get_value_type_int(value_type), 'Verb', verb, 'Qty', qty, 'BookId', '${BOOKID}', 'RecalcFlag', 1)
	BuiltIn().run_keyword('Exec Transaction', get_te_action_record_id(te_action_id), '${TIMEOUT_MSEC}', *transaction_fvs)
	
	trade_id = execute_te_function('SaveTrade', 'S', te_action_id)
	return trade_id