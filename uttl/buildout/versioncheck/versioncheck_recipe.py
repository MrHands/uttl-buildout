import configparser
import logging
import os.path
import re
import subprocess
import types
import zc.buildout
import winreg

from zc.buildout import UserError

class VersionCheckRecipe:
	def __init__(self, buildout, name, options):
		self.buildout, self.name, self.options = buildout, name, options
		self.log = logging.getLogger(self.name)

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

		# create version file

		self.version_path = os.path.join(buildout['buildout']['parts-directory'], self.options['version_file'])

		self.version = configparser.ConfigParser()

		if os.path.exists(self.version_path):
			self.version.read_file(open(self.version_path))
			self.options['path'] = self.version['location']['path']
			self.options['version_major'] = self.version['version']['major']
			self.options['version_minor'] = self.version['version']['minor']
			self.options['version_debug'] = self.version['version']['debug']
		else:
			success, major, minor, debug, self.options['path'] = self.checkVersion()
			if not success:
				raise zc.buildout.UserError('Failed to check version')

			self.version['version'] = {
				'major': str(major),
				'minor': str(minor),
				'debug': str(debug)
			}
			self.version['location'] = {
				'path': self.options['path']
			}

			self.options['version_major'] = self.version['version']['major']
			self.options['version_minor'] = self.version['version']['minor']
			self.options['version_debug'] = self.version['version']['debug']

			with open(self.version_path, 'w+') as f:
				self.version.write(f)

		self.log.debug('path %s version %s.%s.%s' % (self.options['path'], self.options['version_major'], self.options['version_minor'], self.options['version_debug']))

	def install(self):
		self.options.created(self.version_path)

		# check version against required

		self.version.read(self.version_path)

		if int(self.version['version']['major']) < int(self.options['required_major']) or int(self.version['version']['minor']) < int(self.options['required_minor']):
			self.log.error('Dependency at %s.%s is out of date, >= %d.%d is required' % (
				int(self.version['version']['major']),
				int(self.version['version']['minor']),
				int(self.options['required_major']),
				int(self.options['required_minor'])))
			raise zc.buildout.UserError('Version mismatch')

		return self.options.created()

	update = install