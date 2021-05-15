from zc.buildout import UserError
from subprocess import CalledProcessError

import logging
import os
import re
import subprocess

class QmakeRecipe:
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

		self.options.setdefault('executable', 'qmake')

		if not 'vcvars' in self.options:
			raise UserError('Missing mandatory "vcvars" parameter.')

		self.files = self.options['files'].splitlines()
		if not self.files:
			raise UserError('Missing mandatory "files" parameter.')

		self.args = [ ]

		if 'template' in self.options:
			self.args.extend([ '-t', self.options['template'] ])

		if 'template_prefix' in self.options:
			self.args.extend([ '-tp', self.options['template_prefix'] ])

		if 'recursive' in self.options:
			self.args.append('-r')

		if 'artefact_path' in self.options:
			self.args.extend([ '-o', self.options['artefact_path'] ])

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		self.options.created(self.options['artefact_path'])

		if not os.path.exists(self.options['artefact_path']):
			if not self.runCommand(self.args):
				return CalledProcessError

		return self.options.created()

	update = install

	def runCommand(self, args):
		args = [ self.options['vcvars'], 'amd64', '&&', self.options['executable'] ] + args
		args.extend(self.files)

		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				self.log.info(line.rstrip().decode('UTF-8'))

			proc.communicate()

			return proc.returncode == 0