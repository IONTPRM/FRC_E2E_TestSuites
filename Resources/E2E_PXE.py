from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.libraries.Process import Process

import E2E_Utility

def login_to_pxe():
	"""This keyword does login to PXE and verify that trader is ON
	"""
	BuiltIn().run_keyword('Function Define', '${COMMON PXE SRC}', 'VCMILogin', 'User', '${COMMON PXE USER}', 'Pwd', '${COMMON PXE PWD}')
	BuiltIn().run_keyword('Function Set Timeout', '10s')
	BuiltIn().run_keyword('Function Verify Return', '0', 'OK')
	fun_res_obj = BuiltIn().run_keyword('Function Call')
	
	login_record = BuiltIn().run_keyword('Record Define', '${COMMON PXE SRC}', 'CM_LOGIN', '${COMMON PXE CURR}', '${COMMON PXE USER}')
	BuiltIn().run_keyword('Record Set Timeout', login_record, '10s')
	res_obj = BuiltIn().run_keyword('Record Verify Fields', login_record, 'TStatusStr', '==', 'On')
	BuiltIn().run_keyword('Record Subscribe', login_record)
		
def logout_from_pxe():
	"""This keyword does logout from PXE and verify that trader is ON
	"""
	BuiltIn().run_keyword('Function Define', '${COMMON PXE SRC}', 'VCMILogout', 'User', '${COMMON PXE USER}')
	BuiltIn().run_keyword('Function Set Timeout', '10s')
	BuiltIn().run_keyword('Function Verify Return', '0', 'OK')
	fun_res_obj = BuiltIn().run_keyword('Function Call')
	
	login_record = BuiltIn().run_keyword('Record Define', '${COMMON PXE SRC}', 'CM_LOGIN', '${COMMON PXE CURR}', '${COMMON PXE USER}')
	BuiltIn().run_keyword('Record Set Timeout', login_record, '10s')
	BuiltIn().run_keyword('Record Wait Unpublish', login_record)

def feed_refdata_instrument_to_pxe(instr_id):
	"""This keyword performs transaction on FeedToPXE1 field of imported instrument record in Refdata.
	"""
	BuiltIn().run_keyword('Transaction Define', '${COMMON REFDATA SRC}', 'CM_INSTRUMENT', '${COMMON REFDATA CURR}', instr_id)
	BuiltIn().run_keyword('Transaction Set Fields Values', 'FeedToPXE1', '1')
	BuiltIn().run_keyword('Transaction Set Timeout', '5s')
	BuiltIn().run_keyword('Transaction Verify Return', '0', 'Ok')
	BuiltIn().run_keyword('Transaction Call')
	
	# To wait till instrument is published by CM_INSTRUMENT of PXE
	instr_record = BuiltIn().run_keyword('Record Define', '${COMMON PXE SRC}', 'CM_INSTRUMENT', '${COMMON PXE CURR}', instr_id)
	BuiltIn().run_keyword('Record Set Timeout', instr_record, '20s')
	res_obj = BuiltIn().run_keyword('Record Verify Fields', instr_record, 'Id', '==', instr_id)
	BuiltIn().run_keyword('Record Subscribe', instr_record)
	
	BuiltIn().run_keyword('Transaction Define', '${COMMON PXE SRC}', 'CM_INSTRUMENT', '${COMMON PXE CURR}', instr_id)
	BuiltIn().run_keyword('Transaction Set Fields Values', 'Publish', 'true', 'IndicatorProfile', 'EUR')
	BuiltIn().run_keyword('Transaction Set Timeout', '5s')
	BuiltIn().run_keyword('Transaction Verify Return', '0', '0:OK')
	BuiltIn().run_keyword('Transaction Call')

	
def price_instrument_in_pxe(instr_id, value, value_type):
	"""It generate pricing in PXE, call 'CreatePricing' function of PXE passing instrument id to create record in PRICINGS table. 
	Then it transacts on ModelStr, MidPrice fields of PRICING_MAIN table to price this instrument.
	"""
	BuiltIn().run_keyword('Function Define', '${COMMON PXE SRC}', 'CreatePricing', 'BondID', instr_id)
	BuiltIn().run_keyword('Function Set Timeout', '10s')
	BuiltIn().run_keyword('Function Verify RetCode', '0')
	fun_res_obj = BuiltIn().run_keyword('Function Call')
	
	BuiltIn().run_keyword('Transaction Define', '${COMMON PXE SRC}', 'PRICING_MAIN', '${COMMON PXE CURR}', instr_id)
	BuiltIn().run_keyword('Transaction Set Fields Values', 'ModelStr', 'Manual Price')
	BuiltIn().run_keyword('Transaction Set Timeout', '5s')
	BuiltIn().run_keyword('Transaction Verify Return', '0', '0:OK')
	BuiltIn().run_keyword('Transaction Call')
	
	if value_type == 'Price':
		field_name_to_trans_on = 'MidPrice'
	elif value_type == 'Discount':
		field_name_to_trans_on = 'MidDiscount'
	
	BuiltIn().run_keyword('Transaction Define', '${COMMON PXE SRC}', 'PRICING_MAIN', '${COMMON PXE CURR}', instr_id)
	BuiltIn().run_keyword('Transaction Set Fields Values', field_name_to_trans_on, value)
	BuiltIn().run_keyword('Transaction Set Timeout', '5s')
	BuiltIn().run_keyword('Transaction Verify Return', '0', '0:OK')
	BuiltIn().run_keyword('Transaction Call')

anlpycalc_func_res_fieldvalue_pos = {
	'Status':0,
	'Price':1,
	'Yield':2,
	'Discount':3,
	'MMYield':4,
	'DateSettl':5,
	'AccruedInterest':6,
	'AccruedDays':7,
	'DV01':8,
	'IndexRatio':9,
	'RiskPrice':10,
	'DiscountMargin':11,
	'Factor':12}	
	
def get_value_using_anlpycalc_func(fieldname_to_get_value, instr_id, value, value_type, date_settle):
	""" This keyword calls ANLPYCalc function of PXE and return the value for the field you passed as first param 'fieldname_to_get_value'.
	"""
	BuiltIn().run_keyword('Function Define', '${COMMON PXE SRC}', 'ANLPYCalc', 'InstrumentId', instr_id, 'Value', value, 'ValueType', value_type, 'DateSettl', date_settle)
	BuiltIn().run_keyword('Function Set Timeout', '20s')
	BuiltIn().run_keyword('Function Verify Return', '0', 'OK')
	fun_res_obj = BuiltIn().run_keyword('Function Call')
	
	if fieldname_to_get_value in ('Price', 'Yield', 'Discount', 'MMYield', 'AccruedInterest', 'DV01', 'IndexRatio', 'RiskPrice', 'DiscountMargin', 'Factor'):
		field_value_from_anlpycalc = fun_res_obj.getDouble(anlpycalc_func_res_fieldvalue_pos[fieldname_to_get_value])
	elif fieldname_to_get_value in ('DateSettl', 'AccruedDays'):
		field_value_from_anlpycalc = fun_res_obj.getInteger(anlpycalc_func_res_fieldvalue_pos[fieldname_to_get_value])
	
	if E2E_Utility.number_is_nan(field_value_from_anlpycalc):
		return 0.0
		
	return field_value_from_anlpycalc

def remove_instruments_from_pxe(*instr_id_list):
	""" This keyword perform transaction on FeedToPXE1 field of Refdata instrument record which was fed to PXE earlier. 
	By setting FeedToPXE1 to 0, this instrument is removed from PXE tables.
	"""
	for instr in instr_id_list:
		BuiltIn().run_keyword('Transaction Define', '${COMMON REFDATA SRC}', 'CM_INSTRUMENT', '${COMMON REFDATA CURR}', instr)
		BuiltIn().run_keyword('Transaction Set Fields Values', 'FeedToPXE1', '0')
		BuiltIn().run_keyword('Transaction Set Timeout', '5s')
		BuiltIn().run_keyword('Transaction Verify Return', '0', 'Ok')
		BuiltIn().run_keyword('Transaction Call')
