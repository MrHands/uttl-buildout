import logging
import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class CmakeRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		self.options.setdefault('executable', 'cmake')

		self.args = [ ]

		if 'generator' in self.options:
			self.args.extend([ '-G', self.options['generator'] ])

		# configure or build

		if 'configure_path' in self.options:
			self.args.append(os.path.abspath(self.options['configure_path']))
		else:
			if not 'build_path' in self.options:
				raise UserError('Missing mandatory "build_path" parameter.')

			if 'build_path' in self.options:
				build_path = os.path.abspath(self.options['build_path'])
				self.args.extend([ '--build', build_path ])

			if 'target' in self.options:
				targets = self.options['target'].splitlines()
				self.args.extend([ '--target', ' '.join(str(t) for t in targets) ])

			if 'config' in self.options:
				self.args.extend([ '--config', self.options['config'] ])

		self.options['args'] = ' '.join(str(e) for e in self.args)

		# variables

		self.var_args = []

		if 'install_path' in self.options:
			install_path = os.path.abspath(self.options['install_path'])
			self.var_args.append('-DCMAKE_INSTALL_PREFIX=%s' % (install_path))

		if 'variables' in self.options:
			for var in self.options['variables'].splitlines():
				self.var_args.append('-D%s' % (var))

		if 'configure_path' in self.options:
			self.var_args.append(os.path.abspath(self.options['configure_path']))
		elif 'build_path' in self.options:
			self.var_args.append(os.path.abspath(self.options['build_path']))

		self.options['var_args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		# set variables

		if len(self.var_args) > 0:
			args = [ self.options['executable'] ] + self.var_args
			self.runCommand(args, parseLine=self.parseLine, quiet=True)

		# set working directory

		if 'configure_path' in self.options:
			configure_path = os.path.abspath(self.options['configure_path'])

			if not os.path.exists(configure_path):
				os.makedirs(configure_path, 0o777, True)

			self.working_dir = os.getcwd()
			os.chdir(configure_path)

		# run command

		args = [ self.options['executable'] ] + self.args
		self.runCommand(args, parseLine=self.parseLine)

		if 'configure_path' in self.options:
			os.chdir(self.working_dir)

		# add manual artefact (e.g. generated solution)

		if 'artefact_path' in self.options:
			self.options.created(os.path.abspath(self.options['artefact_path']))

		return self.options.created()

	check_errors = re.compile(r'.*Error: (.*)')
	check_failed = re.compile(r'.*(Build FAILED|CMake Error|MSBUILD : error).*')
	check_artefacts = re.compile(r'.*(.+?) -> (.+)')
	check_installed = re.compile(r'.*-- (.+?): (.+)')

	def parseLine(self, line):
		# check for errors

		if self.check_errors.match(line) or self.check_failed.match(line):
			return False

		# add artefacts to options

		match = self.check_artefacts.match(line)
		if match:
			path = match.group(2)
			self.options.created(os.path.abspath(path))

		# add installed files to options

		match = self.check_installed.match(line)
		if match:
			what = match.group(1)
			path = match.group(2)

			if any(what in s for s in ['Installing', 'Up-to-date']):
				self.options.created(os.path.abspath(path))

		return True

def uninstall(name, options):
	pass