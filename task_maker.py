from sys import argv

import os

import templates

options = {
	'--name': None,
	'--path': None
}

def assert_option_present(name):
	if options[name] is None:
		raise ValueError('\n\nRequired argument "{0}" was not specified.\n'.format(name))

def require_dir(path):
	if not os.path.isdir(path):
		os.makedirs(path)

def handle_command_line():
	option_type = options.keys()

	#	skip script name in argv
	idx = 1

	if len(argv) % 2 != 1:
		raise ValueError('\n\nInvalid command line parameter format.\n')

	while idx < len(argv):
		arg = argv[idx]
		opt = argv[idx+1]

		valid_argument = True

		if arg not in option_type:
			print('Unrecognized input "{0}".'.format(arg))
			valid_argument = False

		if valid_argument:
			options[arg] = opt

		idx = idx + 2

def handle_defaults():
	assert_option_present('--name')
	assert_option_present('--path')

def dump_text_to_file(text, file):
	with open(file, 'w') as text_file:
		text_file.write(text)

def get_name():
	return options['--name']

def get_project_folder():
	base_path = options['--path']
	name = get_name()
	return os.path.join(base_path, name)

def get_package_folder():
	project_folder = get_project_folder()
	name = get_name()
	package_name = '+' + name
	return os.path.join(project_folder, package_name)

def get_config_folder():
	package_folder = get_package_folder()
	return os.path.join(package_folder, '+config')

def get_task_folder():
	package_folder = get_package_folder()
	return os.path.join(package_folder, '+task')

def get_util_folder():
	package_folder = get_package_folder()
	return os.path.join(package_folder, '+util')

def get_assert_util_folder():
	return os.path.join(get_util_folder(), '+assertions')

def create_project_folder():
	require_dir(get_project_folder())

def create_package_folder():
	require_dir(get_package_folder())

def create_config_folder():
	require_dir(get_config_folder())

def create_task_folder():
	require_dir(get_task_folder())

def create_util_folders():
	require_dir(get_util_folder())
	require_dir(get_assert_util_folder())

def create_files(sources, outer_folder):
	name = get_name()

	source_keys = sources.keys()

	for source_key in source_keys:
		source_func = sources[source_key]
		source = source_func(name)
		full_file_path = os.path.join(outer_folder, source_key + '.m')
		dump_text_to_file(source, full_file_path)

def create_config_files():
	config_folder = get_config_folder()
	sources = templates.config.get_all()
	create_files(sources, config_folder)

def create_task_files():
	task_folder = get_task_folder()
	sources = templates.task.get_all()
	create_files(sources, task_folder)

def create_util_files():
	util_folder = get_util_folder()
	util_sources = templates.util.get_all()
	create_files(util_sources, util_folder)

	assert_folder = get_assert_util_folder()
	assert_sources = templates.assertions.get_all()
	create_files(assert_sources, assert_folder)

def create_folders():
	create_project_folder()
	create_package_folder()
	create_config_folder()
	create_task_folder()
	create_util_folders()

def main():
	handle_command_line()
	handle_defaults()

	create_folders()

	create_config_files()
	create_task_files()
	create_util_files()

main()