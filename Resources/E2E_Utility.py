import re

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.libraries.Process import Process

from platform_enum import PlatformEnum
from itertools import izip

import E2E_Tradeserver
import E2E_Refdata

DNAN=-9e99
def isnan(num):
	"""Checks for NaN or DNAN; If using python >= 2.6 we could use math.isnan() but math.isnan is unavailable under jython 2.5"""
	return num != num or num == DNAN

def number_is_nan(num):
	"""Checks for NaN or DNAN; If using python >= 2.6 we could use math.isnan() but math.isnan is unavailable under jython 2.5"""
	return isnan(num)
	
def convert_list_into_dict(list):
	i = iter(list)
	return dict(izip(i, i))

wash_name_regex = re.compile('[^a-zA-Z0-9@#_]')
def wash_name(string_to_wash):
	global wash_name_regex
	"return string with ion platform-invalid characters 'washed' to underscores"
	return wash_name_regex.sub('_', string_to_wash)
	
value_type_enum = PlatformEnum({
	'Price' : 1,
	'Yield' : 2,
	'YDIFF' : 4,
	'Basis' : 8,
	'Discount' : 16,
	'Spread' : 32,
	'DiscountMargin' : 64,
	'Undef' : -1})

def get_value_type_str(value_type_int_or_str):
	"""Convert value type into its string equivalent.  Accepts either ints or case insensitive value type."""
	global value_type_enum
	return value_type_enum.get_string(value_type_int_or_str)

def get_value_type_int(value_type_int_or_str):
	"""Convert value type into its integer equivalent.  Accepts either ints or case insensitive value type.  Returns int code as a string."""
	global value_type_enum
	return value_type_enum.get_code(value_type_int_or_str)
	
def get_platform_os():
	""" This keyword returns the operating system type of machine.
	Possible retruns Windows_NT, Linux
	"""
	env_var_dict = BuiltIn().run_keyword('Get Environment Variables')
	plat_os = env_var_dict['OS']
	return plat_os

def select_correct_instrument_to_import(instr_type, coupon_type):
	if instr_type == 'T Note' and coupon_type == 'Fixed':
		ext_instr_id = 'Govt_Fixed_1'
	elif instr_type == 'Corp' and coupon_type == 'Floater':
		ext_instr_id = 'Corp_Floater_1'
	elif instr_type == 'Govt'  and coupon_type == 'Index Linked':
		ext_instr_id = 'Govt_IndexLinked_1'
	elif instr_type == 'Govt'  and coupon_type == 'Sinkable':
		ext_instr_id = 'Govt_Sinakble_1'
	elif instr_type == 'Govt'  and coupon_type == 'Putable':
		ext_instr_id = 'Govt_Putable_1'
	elif instr_type == 'Corp'  and coupon_type == 'Zero Coupon':
		ext_instr_id = 'Corp_ZeroCoupon_1'
	elif instr_type == 'Govt'  and coupon_type == 'Zero Coupon':
		ext_instr_id = 'Govt_ZeroCoupon_1'
	elif instr_type == 'Agency' and coupon_type == 'Fixed':
		ext_instr_id = 'Agency_Fixed_1'
	elif instr_type == 'Agency' and coupon_type == 'Callable':
		ext_instr_id = 'Agency_Callable_1'
	elif instr_type == 'Agency' and coupon_type == 'Zero Coupon':
		ext_instr_id = 'Agency_ZeroCoupon_1'
	
	return ext_instr_id	
	
def cleanup_for_all_imported_instruments(*instr_id_list):
	""" This keyword deletes all trades for an instrument and delete this instrument also.
	"""
	for instr in instr_id_list:
		E2E_Tradeserver.delete_all_trades_for_instrument(instr)
		E2E_Refdata.delete_instrument_from_database(instr)