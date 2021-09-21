from zc.buildout import UserError
from subprocess import CalledProcessError

import logging
import glob
import os
import re
import subprocess

class InklecateRecipe(object):
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

		self.options.setdefault('executable', 'inklecate.exe')
		self.options.setdefault('output_directory', '')

		self.inputs = self.options['inputs'].splitlines()

		self.resolved = []
		for i in self.inputs:
			self.resolved.extend([os.path.abspath(f) for f in glob.glob(i) if os.path.isfile(f)])

		self.options['inputs_resolved'] = ' '.join(str(e) for e in self.resolved)

	def install(self):
		build_inputs = []

		# check if any artefact is missing

		output_directory = self.options['output_directory']

		for i in self.resolved:
			if not os.path.exists(i):
				continue

			filename = os.path.split(i)[1]
			artefact_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.json')

			self.options.created(artefact_path)

			if not os.path.exists(artefact_path):
				build_inputs.append((os.path.abspath(i), artefact_path))
				continue

		# compile

		for ink_in, json_out in build_inputs:
			args = [ self.options['executable'] ]
			args.extend([ '-o', json_out ])
			args.extend([ ink_in ])

			if not self.runCommand(args):
				raise CalledProcessError(0, args)

		return self.options.created()

	update = install

	def runCommand(self, args):
		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				self.log.info(line.rstrip().decode('UTF-8'))

			proc.communicate()

			return proc.returncode == 0

def uninstall(name, options):
	pass