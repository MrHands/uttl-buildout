import logging
import os
import shutil

from uttl.buildout.base_recipe import BaseRecipe
from zc.buildout import UserError

class CopyFileRecipe(BaseRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		self.options.setdefault('source-path', '')
		self.options.setdefault('destination-path', os.getcwd())

		# paths

		self.src_path = os.path.abspath(self.options['source-path'])

		self.dst_path = os.path.abspath(self.options['destination-path'])
		if not os.path.exists(self.dst_path):
			os.makedirs(self.dst_path, 0o777, True)

		# get files

		if not 'files' in self.options:
			raise UserError('Missing mandatory "files" option.')

		self.files = self.options['files'].splitlines()
		self.src_files = [os.path.join(self.src_path, file) for file in self.files]
		self.dst_files = [os.path.join(self.dst_path, file) for file in self.files]

		self.log.debug(str(self.files))

	def install(self):
		installed = self.dst_files
		invalid = []

		# use private api to check for files that need to be installed

		(installed_part_options, installed_exists) = self.buildout._read_installed_part_options()

		if self.name in installed_part_options:
			part_options = installed_part_options[self.name]
			if part_options and '__buildout_installed__' in part_options:
				installed = list(path.rstrip() for path in part_options['__buildout_installed__'].split())

		self.log.debug('installed ' + str(installed))

		invalid = [file for file in installed if not os.path.exists(file)]
		self.log.debug('invalid ' + str(invalid))

		for dst_path in invalid:
			filename = os.path.basename(dst_path)
			src_path = os.path.join(self.src_path, filename)
			self.copyFile(src_path, dst_path, filename)

		# check if files were modified

		check_modified = list(set(invalid) - set(installed))
		self.log.debug('check_modified ' + str(check_modified))
		for dst_path in check_modified:
			filename = os.path.basename(dst_path)

			src_path = os.path.join(self.src_path, filename)
			src_modified = os.path.getmtime(src_path)

			dst_modified = os.path.getmtime(dst_path)

			if src_modified > dst_modified:
				self.log.debug('%s was modified (%d > %d)' % (filename, src_modified, dst_modified))

				self.copyFile(src_path, dst_path, filename)

		"""
		for file in invalid:
			filename = os.path.basename(file)

			src = os.path.abspath(file)
			src_exists = os.path.exists(src)
			if not src_exists:
				src = os.path.abspath(os.path.join(self.src_path, filename))
				src_exists = os.path.exists(src)

			self.log.debug('src: %s (exists: %r)' % (src, src_exists))

			if not src_exists:
				raise FileNotFoundError(src)

			dst = os.path.abspath(os.path.join(self.dst_path, filename))
			dst_exists = os.path.exists(dst)

			self.log.debug('dst: %s (exists: %r)' % (dst, dst_exists))

			self.options.created(dst)

			self.copyFile(src, dst)

		"""
		return self.options.created()

	update = install

	def copyFile(self, src, dst, filename):
		if not os.path.exists(src):
			raise FileNotFoundError(src)

		self.options.created(dst)

		self.log.info('Copying "' + filename + "'...")

		shutil.copy(src, dst)

def uninstall(name, options):
	pass