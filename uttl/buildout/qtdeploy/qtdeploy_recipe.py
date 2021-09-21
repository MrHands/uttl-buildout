import logging
import os.path
import re
import subprocess
import types
import zc.buildout

from zc.buildout import UserError

class QtDeployRecipe(object):
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

		self.options.setdefault('executable', 'windeployqt.exe')

		if not 'vcvars' in self.options:
			raise UserError('Missing mandatory "vcvars" parameter.')

		if not 'target_path' in self.options:
			raise UserError('Missing mandatory "target_path" parameter.')

		self.args = [ ]
		self.args.append(self.options['target_path'])

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		exe_args = [ self.options['vcvars'], 'amd64', '&&', self.options['executable'] ]

		# get list of files

		files = []

		args = exe_args + [ '--list', 'target', self.options['target_path'] ]
		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				path = line.rstrip().decode('UTF-8')

				drive, tail = os.path.splitdrive(path)

				if drive != '':
					files.append(path)

			proc.communicate()

		# copy files

		args = exe_args + [ self.options['target_path'] ]
		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				self.log.info(line.rstrip().decode('UTF-8'))

			proc.communicate()

		# check if files have been copied

		copied = [f for f in files if os.path.exists(f)]
		for f in copied:
			self.options.created(f)

		return self.options.created()

	def update(self):
		pass

def uninstall(name, options):
	pass