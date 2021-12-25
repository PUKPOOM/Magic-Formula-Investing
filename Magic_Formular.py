import csv
import re

import os
import os.path

# -----------------------------------------------------------------------------------
#								F I L E
# -----------------------------------------------------------------------------------
csv_file = 'Stock_Financial_Data_SET100_RE.csv'
##csv_file = 'Stock_Financial_Data_DCA_RE.csv'

file_name = 'Magic_Formular.csv'

# -----------------------------------------------------------------------------------
#								D A T A | S P E C
# -----------------------------------------------------------------------------------
## Not in Information & Communication Technology	by Graham
## Revenue > 10,000M								by Graham
## Assets / Liabilities > 2							by Graham
## EPS > 10											by Graham
## PE < 15											by Graham
## PE x PVB < 22.5									by Graham
## DE Equity % Liabilities < 2.3					by Graham

EPS_enable		= 0
ROA_enable		= 0
ROE_enable		= 0
PE_enable		= 0
PBV_enable		= 0
DE_enable		= 0
DIV_enable		= 1
ASS_LIA_enable	= 0
PE_PBV_enable	= 0

EPS_spec		= 10.0	# digit8
ROA_spec 		= 10.0 	# digit9
ROE_spec 		= 10.0 	# digit10
PE_spec 		= 20.0	# digit14
PBV_spec 		= 10.0 	# digit15
DE_spec 		= 1.0 	# digit4 % digit3
DIV_spec 		= 5.0 	# digit17
ASS_LIA_spec	= 2.0	# digit2 % digit3
PE_PBV_spec 	= 22.3 	# digit14 * digit15

replace_char 	= 'XXX'

def Spec_Data(data, data_row):
	global EPS ; global ROA ; global ROE ; global PE ; global PBV ; global DE ; global DIV ; global ASS_LIA ; global PE_PBV

	if (data_row[8] == '' and EPS_enable) or (data_row[9] == '' and ROA_enable) or (data_row[10] == '' and ROE_enable) or (data_row[14] == '' and PE_enable) or (data_row[15] == '' and PBV_enable) or \
		(data_row[17] == '' and DIV_enable):
		# Data was null or disable spec
		##print('FAIL NULL DATA')
		pass

	else:
		if data_row[8] != '':
			EPS 	= float(data_row[8])
		else:
			EPS 	= 0
		if data_row[9] != '':
			ROA 	= float(data_row[9])
		else:
			ROA 	= 0
		if data_row[10] != '':
			ROE 	= float(data_row[10])
		else:
			ROE 	= 0
		if data_row[14] != '':
			PE 		= float(data_row[14])
		else:
			PE 		= 0
		if data_row[15] != '':
			PBV 	= float(data_row[15])
		else:
			PBV 	= 0
		if data_row[17] != '':
			DIV 	= float(data_row[17])
		else:
			DIV 	= 0

		print('{} : Year {} Date {}'.format(data_row[0], data_row[1][6:10], data_row[1][0:4]))
		print('EPS = {} : Spec > {}'.format(EPS, EPS_spec) if EPS_enable else 'EPS = {}'.format(EPS))
		print('ROA = {} : Spec > {}'.format(ROA, ROA_spec) if ROA_enable else 'ROA = {}'.format(ROA))
		print('ROE = {} : Spec > {}'.format(ROE, ROE_spec) if ROE_enable else 'ROE = {}'.format(ROE))
		print('PE = {} : Spec > {}'.format(PE, PE_spec) if PE_enable else 'PE = {}'.format(PE))
		print('PBV = {} : Spec > {}'.format(PBV, PBV_spec) if PBV_enable else 'PBV = {}'.format(PBV))
		print('DIV = {} : Spec > {}'.format(DIV, DIV_spec) if DIV_enable else 'DIV = {}'.format(DIV))

		if data_row[4] != '' and data_row[3] != '':
			DE 			= round(float(data_row[4]) / float(data_row[3]), 2)
		else:
			DIV 		= 0
		if data_row[2] != '' and data_row[3] != '':
			ASS_LIA 	= round(float(data_row[2]) / float(data_row[3]), 2)
		else:
			ASS_LIA 	= 0
		if data_row[14] != '' and data_row[15] != '':
			PE_PBV 		= round(float(data_row[14]) * float(data_row[15]), 2)
		else:
			PE_PBV 		= 0

		print('DE = {} : Spec < {}'.format(DE, DE_spec) if DE_enable else 'DE = {}'.format(DE))
		print('ASS_LIA = {} : Spec < {}'.format(ASS_LIA, ASS_LIA_spec) if ASS_LIA_enable else 'ASS_LIA = {}'.format(ASS_LIA))
		print('PE_PBV = {} : Spec < {}'.format(PE_PBV, PE_PBV_spec) if PE_PBV_enable else 'PE_PBV = {}'.format(PE_PBV))

		data_row.append(EPS) ; data_row.append(ROA) ; data_row.append(ROE) ; data_row.append(PE) ; data_row.append(PBV) ; data_row.append(DE) ; data_row.append(DIV) ; data_row.append(ASS_LIA) ; data_row.append(PE_PBV)

		if ((EPS < EPS_spec) and EPS_enable) or ((ROA < ROA_spec) and ROA_enable) or ((ROE < ROE_spec) and ROE_enable) or ((PE > PE_spec) and PE_enable) or ((PBV > PBV_spec) and PBV_enable) or \
			((DIV < DIV_spec) and DIV_enable) or ((DE > DE_spec) and DE_enable) or ((ASS_LIA < ASS_LIA_spec) and ASS_LIA_enable) or ((PE_PBV < PE_PBV_spec) and PE_PBV_enable):
			# Data was out of spec or disable spec
			##print('FAIL SPEC')
			pass

		else:
			##print('PASS SPEC')
			data.append(data_row)

	return(data, data_row)

def Read_Data():
	print('=====================\nStart Read Data\n=====================')
	line = 0
	header = {}
	data = []

	f1 = open(csv_file,'r')
	for ii in range(1000):
		print('Line = {}'.format(line))
		line += 1						# increae line number
		full_line = f1.readline()		# read data by line
		txt = full_line.rstrip('\n')	# remove the trailing characters

		if full_line == '':				# no data left, break
			print('End at line : {}\n'.format(line-1))
			break

		if 'NAME' in txt:						# detect header
			header_row = txt.split(',')			# split header by ','
			data.append(header_row)
			print('Data Header : {}\n'.format(data))

			if header == {}:
				for h in header_row:
					header[h] = []					# assign dictionary header
			print('Dictionaty Header : {}\n'.format(header))
		
		else:									# detect data
			data_row = txt.split(',')			# split header by ','
			##print('Raw Data : {}'.format(data_row))

# -----------------------------------------------------------------------------------
#								S C R E E N | D A T A
# -----------------------------------------------------------------------------------
			data, data_row = Spec_Data(data, data_row)
			##print('Screen Data : {}'.format(data))

# -----------------------------------------------------------------------------------
#								D I C T I O N A R Y | D A T A
# -----------------------------------------------------------------------------------
			for j in range(len(header_row)):
					##print('Data Index {} = {}'.format(str(j), data_row[j]))
					data_row[j] = re.sub('"', '', data_row[j])
					header[header_row[j]].append(data_row[j])
			##print('Data Header : {}\n'.format(header))

	f1.close()

	print('=====================\nFinish Read Data\n=====================')
	##print('Data Dictionary : {}\n'.format(header))
	##print('Pass Screen Data : {}\n'.format(data))
	print('Number of Columns : {}'.format(len(header)))
	print('Number of Rows : {}\n'.format(len(header['NAME'])))

# -----------------------------------------------------------------------------------
#								P R I N T | S P E C
# -----------------------------------------------------------------------------------
	print('=====================\nEnable Spec\n=====================')
	if EPS_enable:
		print('Digit 8 : {} Spec > {}'.format(header_row[8], EPS_spec))
	if ROA_enable:
		print('Digit 9 : {} Spec > {}'.format(header_row[9], ROA_spec))
	if ROE_enable:
		print('Digit 10 : {} Spec > {}'.format(header_row[10], ROE_spec))
	if PE_enable:
		print('Digit 14 : {} Spec < {}'.format(header_row[14], PE_spec))
	if PBV_enable:
		print('Digit 15 : {} Spec < {}'.format(header_row[15], PBV_spec))		
	if DE_enable:
		print('Digit 4/3 : {} Spec < {}'.format('DE', DE_spec))
	if DIV_enable:
		print('Digit 17 : {} Spec > {}'.format(header_row[17], DIV_spec))
	if ASS_LIA_enable:
		print('Digit 2/3 : {} Spec > {}'.format('Assets / Liabilities', ASS_LIA_spec))
	if PE_PBV_enable:
		print('Digit 14x15 : {} Spec > {}'.format('PE x PBV', PE_PBV_spec))
	print()

	return(data)

def Write_Data(data):
	print('=====================\nStart Write CSV\n=====================')
	stocks_name = []
	stocks_pass = []
	name = ''

	for i in data:
		stocks_name.append(i[0])	# Save only NAME to list

	for i in stocks_name:
		if name == i:				# Skip duplicate NAME
			pass
		else:
			count = stocks_name.count(i)			# Count how many duplicate NAME 
			##print('{} Count = {}'.format(i, count))
			stocks_pass.append([i, count])			# Save only single NAME to list
		name = i 					# Save latest NAME

	print('Number of Data : {}'.format(len(data)))
	print('Number of Stocks : {}'.format(len(stocks_pass)))
	print(stocks_pass)
	print()

	file_exists = os.path.isfile(file_name)
	if file_exists:
		os.remove(file_name)		# Alway write a new file
	with open(file_name,'a', newline="") as f:
		fw = csv.writer(f)
		row_list = []
		for i in data:
			if i[0] == 'NAME':		# Write header
				row_list = ['NAME', 'YEAR', 'DATE', 'ROE(%)', 'P/E', 'Dvd. Yield(%)', 'Industry', 'Sector']
				if EPS_enable: row_list.append('EPS')
				if ROA_enable: row_list.append('ROA%')
				if ROE_enable: row_list.append('ROE%')
				if PE_enable: row_list.append('P/E')
				if PBV_enable: row_list.append('P/BV')
				if DE_enable: row_list.append('D/E')
				if DIV_enable: row_list.append('DIV%')
				if ASS_LIA_enable: row_list.append('ASS/LIA')
				if PE_PBV_enable: row_list.append('PExPBV')
				fw.writerow(row_list)
			else:					# Write data
				row_list = [i[0], i[1][6:10], i[1][0:4], i[10], i[14], i[17], i[18], i[19]]
				if EPS_enable: row_list.append(i[20])
				if ROA_enable: row_list.append(i[21])
				if ROE_enable: row_list.append(i[22])
				if PE_enable: row_list.append(i[23])
				if PBV_enable: row_list.append(i[24])
				if DE_enable: row_list.append(i[25])
				if DIV_enable: row_list.append(i[26])
				if ASS_LIA_enable: row_list.append(i[27])
				if PE_PBV_enable: row_list.append(i[28])
				fw.writerow(row_list)

	print('=====================\nEnd Write CSV\n=====================')

# -----------------------------------------------------------------------------------
#								M A I N | P R O G R A M
# -----------------------------------------------------------------------------------

stock_data = Read_Data()
Write_Data(stock_data)