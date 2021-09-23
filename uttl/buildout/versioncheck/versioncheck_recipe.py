import configparser
import os.path
import re
import subprocess
import types

from uttl.buildout.base_recipe import BaseRecipe
from zc.buildout import UserError

class VersionCheckRecipe(BaseRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		self.options.setdefault('version_file', name + '.ini')
		self.options.setdefault('required_major', '0')
		self.options.setdefault('required_minor', '0')
		self.options.setdefault('version_major', '0')
		self.options.setdefault('version_minor', '0')
		self.options.setdefault('version_debug', '0')

		# convert body into function
		# adapted from mr.scripty

		newbody = 'def checkVersion(self):\n'
		indent = True
		for line in self.options['body'].split('\n'):
			if line.startswith("..."):
				line = line[4:]
			if indent:
				newbody += "  "
				newbody += line + '\n'
			if line.startswith('"""'):
				indent = not indent

		exec(newbody, globals(), locals())
		f = types.MethodType(eval('checkVersion'), self)
		setattr(self, 'checkVersion', f)

		# version file

		self.version_file = os.path.join(buildout['buildout']['parts-directory'], self.options['version_file'])

		# check version using script method

		success, self.version_major, self.version_minor, self.version_debug, self.path = self.checkVersion()
		if not success:
			raise UserError('Failed to check version.')

		self.options['version_major'] = str(self.version_major)
		self.options['version_minor'] = str(self.version_minor)
		self.options['version_debug'] = str(self.version_debug)
		self.options['path'] = self.path

		self.log.debug('path %s version %s.%s.%s' % (self.options['path'], self.options['version_major'], self.options['version_minor'], self.options['version_debug']))

	def install(self):
		self.options.created(self.version_file)

		# read or create version object

		self.version = configparser.ConfigParser()
		if os.path.exists(self.version_file):
			self.version.read_file(open(self.version_file))
		else:
			self.version['version'] = {
				'major': '0',
				'minor': '0',
				'debug': '0'
			}

		# check for newer version

		if int(self.options['version_major']) > int(self.version['version']['major']) or int(self.options['version_minor']) > int(self.version['version']['minor']) or int(self.options['version_debug']) > int(self.version['version']['debug']):
			version_old = '%s.%s.%s' % (self.version['version']['major'], self.version['version']['minor'], self.version['version']['debug'])
			version_new = '%s.%s.%s' % (self.options['version_major'], self.options['version_minor'], self.options['version_debug'])
			self.log.info('Found newer version: %s > %s' % (version_old, version_new))

			self.version['version'] = {
				'major': self.options['version_major'],
				'minor': self.options['version_minor'],
				'debug': self.options['version_debug']
			}
			self.version['location'] = {
				'path': self.options['path']
			}

			with open(self.version_file, 'w+') as f:
				self.version.write(f)

		# check version against required

		if int(self.version['version']['major']) < int(self.options['required_major']) or int(self.version['version']['minor']) < int(self.options['required_minor']):
			self.log.error('Dependency at %s.%s is out of date, >= %d.%d is required' % (
				int(self.version['version']['major']),
				int(self.version['version']['minor']),
				int(self.options['required_major']),
				int(self.options['required_minor'])))
			raise UserError('Version mismatch')

		return self.options.created()

	update = install

def uninstall(name, options):
	pass