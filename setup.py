from setuptools import setup, find_packages

def get_text_from_file(fn):
	text = open(fn, 'rb').read()
	return text.decode('utf-8')

setup(name = 'uttl.buildout',
	version = '1.0.0',
	description = 'Utilities for Buildout developed for Up There They Love.',
	long_description = '\n\n'.join([
		get_text_from_file('README.md'),
		get_text_from_file('CHANGES.md')]),
	keywords = 'buildout extension uttl cmake qmake qt copyfile version',
	author = 'Mr. Hands',
	author_email = 'mrhands31@gmail.com',
	url = 'https://github.com/MrHands/uttl-buildout',
	license = 'MIT',
	packages = find_packages(),
	namespace_packages = [ 'uttl' ],
	include_package_data = True,
	zip_safe = False,
	install_requires = [
		'setuptools',
		'zc.buildout'
	],
	tests_require = [ 'mock' ],
	python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
	test_suite = 'uttl.buildout.tests',
	entry_points = { 
		'zc.buildout': [
			'cmake = uttl.buildout.cmake.cmake_recipe:CmakeRecipe',
			'copyfile = uttl.buildout.copyfile.copyfile_recipe:CopyFileRecipe',
			'devenv = uttl.buildout.devenv.devenv_recipe:DevenvRecipe',
			'dotnet = uttl.buildout.dotnet.dotnet_recipe:DotnetRecipe',
			'inklecate = uttl.buildout.inklecate.inklecate_recipe:InklecateRecipe',
			'qmake = uttl.buildout.qmake.qmake_recipe:QmakeRecipe',
			'qtdeploy = uttl.buildout.qtdeploy.qtdeploy_recipe:QtDeployRecipe',
			'versioncheck = uttl.buildout.versioncheck.versioncheck_recipe:VersionCheckRecipe',
		],
		'zc.buildout.uninstall': [
			'cmake = uttl.buildout.cmake.cmake_recipe:uninstall',
			'copyfile = uttl.buildout.copyfile.copyfile_recipe:uninstall',
			'devenv = uttl.buildout.devenv.devenv_recipe:uninstall',
			'dotnet = uttl.buildout.dotnet.dotnet_recipe:uninstall',
			'inklecate = uttl.buildout.inklecate.inklecate_recipe:uninstall',
			'qmake = uttl.buildout.qmake.qmake_recipe:uninstall',
			'qtdeploy = uttl.buildout.qtdeploy.qtdeploy_recipe:uninstall',
			'versioncheck = uttl.buildout.versioncheck.versioncheck_recipe:uninstall',
		]
	},
	)