import logging
import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe

class CmakeRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		self.options.setdefault('executable', 'cmake')

		self.args = [ ]

		if 'generator' in self.options:
			self.args.extend([ '-G', self.options['generator'] ])

		if 'configure_path' in self.options:
			self.args.append(os.path.abspath(self.options['configure_path']))

		build_path = os.path.abspath(self.options['build_path']) if 'build_path' in self.options else None
		install_path = os.path.abspath(self.options['install_path']) if 'install_path' in self.options else None

		if build_path:
			self.args.extend([ '--build', build_path ])
		elif install_path:
			self.args.extend([ '--build', install_path ])

		if 'target' in self.options:
			self.args.extend([ '--target', self.options['target'] ])

		if 'config' in self.options:
			self.args.extend([ '--config', self.options['config'] ])

		# variables

		if install_path:
			self.args.append('-DCMAKE_INSTALL_PREFIX=' + install_path)

		if 'variables' in self.options:
			for var in self.options['variables'].splitlines():
				self.args.append('-D%s' % var)

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		if 'configure_path' in self.options:
			configure_path = os.path.abspath(self.options['configure_path'])

			if not os.path.exists(configure_path):
				os.makedirs(configure_path, 0o777, True)

			self.working_dir = os.getcwd()
			os.chdir(configure_path)

		self.runCommand(self.args)

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

	def runCommand(self, args):
		args = [ self.options['executable'] ] + args
		
		success = True

		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				stripped = line.rstrip().decode('UTF-8')

				# check for errors

				if self.check_errors.match(stripped) or self.check_failed.match(stripped):
					success = False

				# add artefacts to options

				match = self.check_artefacts.match(stripped)
				if match:
					path = match.group(2)
					self.options.created(os.path.abspath(path))

				# add installed files to options

				match = self.check_installed.match(stripped)
				if match:
					what = match.group(1)
					path = match.group(2)

					if any(what in s for s in ['Installing', 'Up-to-date']):
						self.options.created(os.path.abspath(path))

				self.log.info(stripped)

			proc.communicate()

		return success

def uninstall(name, options):
	pass