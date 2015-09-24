from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.DateTime import Date
from robot.libraries.DateTime import Time
from robot.libraries.Process import Process

def get_instrument_id_of_imported_instrument(external_id):
	"""It returns the Refdata instrument id of the imported instrument.
	It requires id of external instrument published by external source.
	"""
	BuiltIn().run_keyword('Start Platform Component', '${COMMON DPLAYER BBGMDATA COMP NAME}') 
	refdata_instr_id = BuiltIn().run_keyword('Get Field Value From Record', '${COMMON REFDATA SRC}', '${COMMON REFDATA CURR}', 'INSTRUMENTMAPPING', '${COMMON DPLAYER BBGMDATA SRC}' + '_' + external_id, 'TargetId', '${TIMEOUT_SEC}')
	return refdata_instr_id
	
def configure_refdata_with_bbg_dplayer_as_extins_source():
	"""This keyword configures external source in Refdata so that instruments being published external source should be imported by Refdata.
	It configures MAPPING_SOURCES, MAPPING_CURRENCIES, EXTINS_SOURCES, EXTINS_CURRENCIES, EXTINS_MAPPINGMODE(<source>) and EXTINS_INSERTMODE(<source>).
	If these variables are already set, Refdata is not restarted otherwise it restarts the Refdata also.
	"""
	is_restart_required = 0
	status, extins_insertmode = BuiltIn().run_keyword('Run Keyword And Ignore Error', 'Dplayer', 'Get Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_INSERTMODE(${COMMON DPLAYER BBGMDATA SRC})')
	if status == 'PASS':
		if extins_insertmode == 0:
			BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_INSERTMODE(${COMMON DPLAYER BBGMDATA SRC})', '1')
			is_restart_required = 1
	else:
		BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_INSERTMODE(${COMMON DPLAYER BBGMDATA SRC})', '1')
		is_restart_required = 1

	status, extins_mappingmode = BuiltIn().run_keyword('Run Keyword And Ignore Error', 'Dplayer', 'Get Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_MAPPINGMODE(${COMMON DPLAYER BBGMDATA SRC})')
	if status == 'PASS':
		if extins_mappingmode == 0:
			BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_MAPPINGMODE(${COMMON DPLAYER BBGMDATA SRC})', '1')
			is_restart_required = 1
	else:
		BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_MAPPINGMODE(${COMMON DPLAYER BBGMDATA SRC})', '1')
		is_restart_required = 1
		
	current_mapping_sources = BuiltIn().run_keyword('Dplayer', 'Get Component Setting', '${COMMON REFDATA COMP NAME}', 'MAPPING_SOURCES')
	current_mapping_curr = BuiltIn().run_keyword('Dplayer', 'Get Component Setting', '${COMMON REFDATA COMP NAME}', 'MAPPING_CURRENCIES')
	current_extins_sources = BuiltIn().run_keyword('Dplayer', 'Get Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_SOURCES')
	current_extins_curr = BuiltIn().run_keyword('Dplayer', 'Get Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_CURRENCIES')
	current_mapping_sources_list = current_mapping_sources.split()
	current_mapping_curr_list = current_mapping_curr.split()
	current_extins_sources_list = current_extins_sources.split()
	current_extins_curr_list = current_extins_curr.split()
	
	is_bbg_dplayer_src_set_in_mapping_sources = 0
	is_bbg_dplayer_src_set_in_extins_sources = 0
	bbg_dplayer_src = BuiltIn().run_keyword('Get Variable Value', '${COMMON DPLAYER BBGMDATA SRC}')
	for val in current_mapping_sources_list:
		if val == bbg_dplayer_src:
			is_bbg_dplayer_src_set_in_mapping_sources = 1
			break

	for val in current_extins_sources_list:
		if val == bbg_dplayer_src:
			is_bbg_dplayer_src_set_in_extins_sources = 1
			break
			
	if is_bbg_dplayer_src_set_in_mapping_sources == 0:
		BuiltIn().run_keyword('Log', 'Mapping source for BBG Dplayer is not set, configuring it now')
		current_mapping_sources_list.append('${COMMON DPLAYER BBGMDATA SRC}')
		current_mapping_curr_list.append('${COMMON DPLAYER BBGMDATA CURR}')
		
		updated_mapping_sources = ' '.join(current_mapping_sources_list)
		updated_mapping_curr = ' '.join(current_mapping_curr_list)
	
		BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'MAPPING_SOURCES', updated_mapping_sources)
		BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'MAPPING_CURRENCIES', updated_mapping_curr)
		is_restart_required = 1
		
	if	is_bbg_dplayer_src_set_in_extins_sources == 0:
		BuiltIn().run_keyword('Log', 'Extins source for BBG Dplayer is not set, configuring it now')
		current_extins_sources_list.append('${COMMON DPLAYER BBGMDATA SRC}')
		current_extins_curr_list.append('${COMMON DPLAYER BBGMDATA CURR}')
		
		updated_extins_sources = ' '.join(current_extins_sources_list)
		updated_extins_curr = ' '.join(current_extins_curr_list)
	
		BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_SOURCES', updated_extins_sources)
		BuiltIn().run_keyword('Dplayer', 'Set Component Setting', '${COMMON REFDATA COMP NAME}', 'EXTINS_CURRENCIES', updated_extins_curr)
		is_restart_required = 1
		
	if is_restart_required == 1:
		BuiltIn().run_keyword('Dplayer', 'Stop Component', '${COMMON REFDATA COMP NAME}')
		BuiltIn().run_keyword('Dplayer', 'Wait For Component To Stop', '${COMMON REFDATA COMP NAME}')
		
		BuiltIn().run_keyword('Dplayer', 'Start Component', '${COMMON REFDATA COMP NAME}')
		BuiltIn().run_keyword('Dplayer', 'Wait For Component To Start', '${COMMON REFDATA COMP NAME}')

	else:
		BuiltIn().run_keyword('Log', 'BBG Dplayer source is already set in Refdata')

def delete_instrument_from_database(instr_id):
	""" This keyword deletes instrument record from database.
	"""
	where_clause = '%s%s\'%s\'' % ('sec_id', '=', instr_id)
	BuiltIn().run_keyword('SQL Connect To DBMS', '${DB TYPE}', '${DB HOST}', '${DB PORT}', '${DB NAME}', '${DB USER}', '${DB PWD}')
	
	instrument_table_list = ['FW_bond_desc', 'FW_corp_desc', 'FW_agency_desc', 'FW_futures_desc']
	for table in instrument_table_list:
		BuiltIn().run_keyword('SQL Delete Record', table, where_clause)
	
	BuiltIn().run_keyword('SQL Execute Procedure', 'commit')
	BuiltIn().run_keyword('SQL Disconnect from DBMS')	