# encoding: utf-8

import os
from config import path_to_teambeam_executable


def add_paper(file):
	os.system('cd ' + path_to_teambeam_executable + ' &&  sh pdf-to-xml -a ' + file)
