import logging
import os
import re
import subprocess

class CmakeRecipe:
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

		self.args = [ ]

		if 'generator' in self.options:
			self.args.extend([ '-G', self.options['generator'] ])

		if 'configure_path' in self.options:
			self.args.append(self.options['configure_path'])

		if 'install_path' in self.options:
			self.args.append('-DCMAKE_INSTALL_PREFIX=' + os.path.abspath(self.options['install_path']))

		if 'flags' in self.options:
			self.args.append(self.options['flags'])

		dirs = [dir for dir in list(self.options.keys()) if dir.endswith('_DIR')]
		for dir in dirs:
			self.args.append('-D%s:PATH=%s' % (dir, os.path.abspath(self.options[dir])))

		if 'build_path' in self.options:
			self.args.extend([ '--build', self.options['build_path'] ])
		elif 'source_path' in self.options:
			self.args.extend([ '--build', self.options['source_path'] ])

		if 'target' in self.options:
			self.args.extend([ '--target', self.options['target'] ])

		if 'config' in self.options:
			self.args.extend([ '--config', self.options['config'] ])

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		self.options.created(self.options['artefact_path'])

		if not os.path.exists(self.options['artefact_path']):
			if 'configure_path' in self.options:
				self.working_dir = os.getcwd()
				os.chdir(os.path.abspath(self.options['configure_path']))

			self.runCommand(self.args)

			if 'configure_path' in self.options:
				os.chdir(self.working_dir)

		return self.options.created()

	update = install

	def runCommand(self, args):
		args = [ 'cmake' ] + args
		error_check = re.compile('.*Error: (.*)')
		build_check = re.compile('.*(Build FAILED|CMake Error|MSBUILD : error).*')
		success = True

		self.log.debug(str(args))

		with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
			for line in iter(proc.stdout.readline, b''):
				stripped = line.rstrip().decode('UTF-8')

				if error_check.match(stripped) or build_check.match(stripped):
					success = False

				self.log.info(stripped)

			proc.communicate()

		return success