from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.libraries.Process import Process

from function_error_exception import FunctionErrorException
import E2E_Utility
import E2E_PXE

_ts_trade_table_prefix = '${TRADESERVER CURR}.CM_TRADE.${TRADESERVER SRC}' 
def get_ts_trade_record_id(ts_trade_id):
	washed_trade_id = E2E_Utility.wash_name(ts_trade_id)
	return '%s.%s' % (_ts_trade_table_prefix, washed_trade_id)
	
def verify_tradeserver_fields(trade_id, *fvpairs):
	""" This keyword verifies CM_TRADE record fields, we pass trade_id and paired list of fields and values.
	"""
	cm_trade_record_name = get_ts_trade_record_id(trade_id)
	
	# converted list of field values pairs into a dictionary
	fvpairs_dict = E2E_Utility.convert_list_into_dict(fvpairs)
	
	# to get values for params to pass to ANLPYCalc function
	instr_id = BuiltIn().run_keyword('Get record Value', cm_trade_record_name, 5000, 'InstrumentId')
	value = BuiltIn().run_keyword('Get record Value', cm_trade_record_name, 5000, 'Value')
	value_type = BuiltIn().run_keyword('Get record Value', cm_trade_record_name, 5000, 'ValueType')
	date_settle = BuiltIn().run_keyword('Get record Value', cm_trade_record_name, 5000, 'DateSettl')
		
	# replaced 'value_ret_by_pxe' string by corresponding value returned by PXE ANLPYCalc function
	for key, val in fvpairs_dict.iteritems():
		if val == 'value_ret_by_pxe':
			fvpairs_dict[key] = E2E_PXE.get_value_using_anlpycalc_func(key, instr_id, value, value_type, date_settle)
	
	# to prepared list from dictionary of fields & values	
	fvpairs_list = list(reduce(lambda x, y: x + y, fvpairs_dict.items()))
		
	BuiltIn().run_keyword('Test Record', cm_trade_record_name, 5000, fvpairs_list)
	
def delete_all_trades_for_instrument(instr_id):
	"""This keyword deletes all trades for an instrument from database.
	"""
	where_clause = '%s%s\'%s\'' % ('sec_id', '=', instr_id)
	BuiltIn().run_keyword('SQL Connect To DBMS', '${DB TYPE}', '${DB HOST}', '${DB PORT}', '${DB NAME}', '${DB USER}', '${DB PWD}')
	BuiltIn().run_keyword('SQL Delete Record', 'FW_trade', where_clause)
	BuiltIn().run_keyword('SQL Delete Record', 'FW_trade_archive', where_clause)
	BuiltIn().run_keyword('SQL Execute Procedure', 'commit')
	BuiltIn().run_keyword('SQL Disconnect from DBMS')