from setuptools import setup, find_packages

def get_text_from_file(fn):
	text = open(fn, 'rb').read()
	return text.decode('utf-8')

setup(name = 'uttl-buildout',
	version = '1.0.0',
	description = 'Utilities for Buildout developed for Up There They Love.',
	long_description = '\n\n'.join([
		get_text_from_file('README.md'),
		get_text_from_file('CHANGES.md')]),
	keywords = 'buildout extension vcs develop',
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
			'versioncheck = uttl.buildout.versioncheck.versioncheck_recipe:VersionCheckRecipe',
		]
	},
	)