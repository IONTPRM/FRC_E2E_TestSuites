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
import E2E_Tradeserver

_risk_pnldetails_table_prefix = '${RISK CURR}.PNLDETAILS.${RISK SRC}' 
def get_pnldetails_record_id(book_id, instr_id, date_settl):
	return '%s.%s_%s_%s____' % (_risk_pnldetails_table_prefix, book_id, instr_id, date_settl)
	
def verify_risk_fields(instr_id, trade_id, *fvpairs):
	""" This keyword verifies POSITIONDETAILS record fields, we pass instr_id and paired list of fields and values.
	"""
	
	cm_trade_record_name = E2E_Tradeserver.get_ts_trade_record_id(trade_id)
	date_settle = BuiltIn().run_keyword('Get record Value', cm_trade_record_name, 5000, 'DateSettl')

	pnldetails_record_name = get_pnldetails_record_id('${BOOKID}', instr_id, date_settle)
		
	BuiltIn().run_keyword('Test Record', pnldetails_record_name, 5000, fvpairs)