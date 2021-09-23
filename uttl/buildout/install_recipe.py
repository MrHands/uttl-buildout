import os
import subprocess

from subprocess import CalledProcessError
from uttl.buildout.base_recipe import BaseRecipe

class InstallRecipe(BaseRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

	def update(self):
		if 'always_install' in self.options and self.options['always_install'] == '1':
			return self.install()

		# use private api to check for files that need to be installed

		(installed_part_options, installed_exists) = self.buildout._read_installed_part_options()

		part_options = installed_part_options[self.name]
		if not part_options:
			self.log.info('Installing again due to missing options.')
			return self.install()

		if not '__buildout_installed__' in part_options:
			self.log.info('No files were installed previously.')
			return self.install()

		installed = (path.rstrip() for path in part_options['__buildout_installed__'].split())
		for path in installed:
			if not os.path.exists(path):
				self.log.info('Installing again due to missing file.')
				self.log.debug('MISSING: %s' % (path))
				return self.install()

	def runCommand(self, args, parseLine=lambda line: True, quiet=False, expected=0):
		success = True

		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				stripped = line.rstrip().decode('UTF-8')

				if not quiet:
					self.log.info(stripped)

				if not parseLine(stripped):
					success = False

			proc.communicate()

			self.log.debug('returned %d' % (proc.returncode))

			if proc.returncode != expected:
				raise CalledProcessError(0, args)

		return success