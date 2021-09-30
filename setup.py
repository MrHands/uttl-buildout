from setuptools import setup, find_packages
from contextlib import contextmanager
import os.path
import os

@contextmanager
def change_dir(path):
	current = os.path.abspath(os.curdir)
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(current)

# decorator for running functions inside the setup dir

def in_setup_dir(fn):
	setup_dir = os.path.dirname(os.path.abspath(__file__))

	def wrapped(*args, **kwargs):
		with change_dir(setup_dir):
			return fn(*args, **kwargs)

	return wrapped

@in_setup_dir
def get_text_from_file(path):
	return open(path, encoding='utf-8').read()

setup(name = 'uttl.buildout',
	version = '1.2.4',
	description = 'Utilities for Buildout developed for Up There They Love.',
	long_description =
		get_text_from_file('README.md') +
		get_text_from_file('CHANGES.md') +
		"\n# License\n\n" +
		get_text_from_file('LICENSE'),
	long_description_content_type = 'text/markdown',
	keywords = 'buildout extension uttl cmake qmake qt copyfile version',
	classifiers = [
		'Framework :: Buildout',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT No Attribution License (MIT-0)',
	],
	author = 'Mr. Hands',
	author_email = 'mrhands31@gmail.com',
	url = 'https://github.com/MrHands/uttl-buildout',
	license = 'MIT-0',
	packages = find_packages(),
	namespace_packages = [ 'uttl' ],
	include_package_data = True,
	zip_safe = False,
	install_requires = [
		'setuptools',
		'zc.buildout'
	],
	tests_require = [ 'mock' ],
	python_requires = '>=3',
	test_suite = 'uttl.buildout.tests',
	entry_points = { 
		'zc.buildout': [
			'cmake = uttl.buildout.cmake.cmake_recipe:CmakeRecipe',
			'command = uttl.buildout.command_recipe:CommandRecipe',
			'copyfile = uttl.buildout.copyfile.copyfile_recipe:CopyFileRecipe',
			'devenv = uttl.buildout.devenv.devenv_recipe:DevenvRecipe',
			'dotnet-restore = uttl.buildout.dotnet.restore.dotnet_restore_recipe:DotnetRestoreRecipe',
			'inklecate = uttl.buildout.inklecate.inklecate_recipe:InklecateRecipe',
			'qmake = uttl.buildout.qmake.qmake_recipe:QmakeRecipe',
			'qtdeploy = uttl.buildout.qtdeploy.qtdeploy_recipe:QtDeployRecipe',
			'versioncheck = uttl.buildout.versioncheck.versioncheck_recipe:VersionCheckRecipe',
		],
		'zc.buildout.uninstall': [
			'cmake = uttl.buildout.cmake.cmake_recipe:uninstall',
			'command = uttl.buildout.command_recipe:uninstall',
			'copyfile = uttl.buildout.copyfile.copyfile_recipe:uninstall',
			'devenv = uttl.buildout.devenv.devenv_recipe:uninstall',
			'dotnet-restore = uttl.buildout.dotnet.restore.dotnet_restore_recipe:uninstall',
			'inklecate = uttl.buildout.inklecate.inklecate_recipe:uninstall',
			'qmake = uttl.buildout.qmake.qmake_recipe:uninstall',
			'qtdeploy = uttl.buildout.qtdeploy.qtdeploy_recipe:uninstall',
			'versioncheck = uttl.buildout.versioncheck.versioncheck_recipe:uninstall',
		]
	},
)