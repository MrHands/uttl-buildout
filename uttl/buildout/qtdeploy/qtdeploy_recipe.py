import logging
import os.path
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class QtDeployRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		self.options.setdefault('executable', 'windeployqt.exe')

		if not 'target_path' in self.options:
			raise UserError('Missing mandatory "target_path" parameter.')

		self.args = [ ]

		if 'translations' in self.options:
			translations = self.options['translations'].splitlines()
			self.args.append(','.join(str(t) for t in translations))
		else:
			self.args.append('--no-translations')

		self.args.append(self.options['target_path'])
		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		# build argument list

		exe_args = []

		if 'vcvars' in self.options:
			exe_args += [ self.options['vcvars'], 'amd64', '&&' ]

		exe_args.append(self.options['executable'])

		# get list of files

		files = []

		args = exe_args + [ '--list', 'target' ] + self.args
		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				path = line.rstrip().decode('UTF-8')

				drive, tail = os.path.splitdrive(path)

				if drive != '':
					files.append(path)

			proc.communicate()

		# copy files

		args = exe_args + self.args
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