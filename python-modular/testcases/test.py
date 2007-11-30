#!/usr/bin/env python

from numpy import *
import sys

import kernels
import distances

SUPPORTED=['kernels', 'distances']

def _get_name_fun (fnam):
	module=None

	for s in SUPPORTED:
		if fnam.find(s)>-1:
			module=s
			break

	if module is None:
		print 'Module %s not supported yet!'%name
		return None

	return module+'.test'

def _test_mfile (fnam):
	mfile=open(fnam, mode='r')
	input={}

	name_fun=_get_name_fun(fnam)
	for line in mfile:
		param = line.split('=')[0].strip()
		
		if param=='name':
			name=line.split('=')[1].strip().split("'")[1]
			input[param]=name
		elif param=='symdata' or param=='data':
			input[param]=_read_matrix(line)
		elif param.startswith('km_') or param.startswith('dm_'):
			input[param]=_read_matrix(line)
		elif param.find('data_train')>-1 or param.find('data_test')>-1:
			input[param]=_read_matrix(line)
		else:
			if (line.find("'")==-1):
				input[param]=eval(line.split('=')[1])
			else: 
				input[param]=line.split('=')[1].strip().split("'")[1]

	mfile.close()
	fun=eval(name_fun)

	return fun(input)

def _read_matrix (line):
	str=(line.split('[')[1]).split(']')[0]
	lines=str.split(';')
	lis2d=list()

	for x in lines:
		lis=list()
		for y in x.split(','):
			y=y.replace("'","").strip()
			if(y.isalpha()):
				lis.append(y)
			else:
				if y.find('.')!=-1:
					lis.append(float(y))
				else:
					lis.append(int(y))
		lis2d.append(lis)

	return array(lis2d)

for fnam in sys.argv:
	if (fnam.endswith('.m')):
		res=_test_mfile(fnam)
		if res:
			sys.exit(0)
		else:
			sys.exit(1)
