import os

from uttl.buildout.base_recipe import BaseRecipe

class InstallRecipe(BaseRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

	def update(self):
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