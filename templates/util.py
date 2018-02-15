def print_error_stack(name):
	return r"""
function print_error_stack( err )

%	PRINT_ERROR_STACK -- Print a stack trace on error.

if ( ~isa(err, 'MException') ), return; end;

stack = err.stack;
max_line_chars = 0;
for i = 1:numel(stack)
  max_line_chars = max( max_line_chars, numel(num2str(stack(i).line)) );
end

fprintf( '\n\n\nError traceback:\n' );
for i = numel(stack):-1:1
  extra_spaces = max_line_chars - numel( num2str(stack(i).line) );
  if ( extra_spaces == 0 )
    extra_spaces = '';
  else extra_spaces = repmat( ' ', 1, extra_spaces );
  end
  fprintf( '\n - %d,%s %s', stack(i).line, extra_spaces, stack(i).name );
end

fprintf( '\n\n - Message: %s\n\n\n', err.message );

end"""

def add_depends(name):
  return r"""
function add_depends()

%   ADD_DEPENDS -- Add dependencies as defined in the config file.

conf = {0}.config.load();

repos = conf.DEPENDS.repositories;
repo_dir = conf.PATHS.repositories;

for i = 1:numel(repos)
  addpath( genpath(fullfile(repo_dir, repos{{i}})) );
end

end""".format(name)

def get_project_folder(name):
    return r"""
function out = get_project_folder()

%   GET_PROJECT_FOLDER -- Get the path to the folder containing the package "{0}".
%
%       OUT:
%           - `out` (char)

path_components = fileparts( which('{0}.util.get_project_folder') );

if ( ispc() )
    slash = '\';
else
    slash = '/';
end

path_components = strsplit( path_components, slash );
path_components = path_components(1:end-2);

out = strjoin( path_components, slash );

end""".format(name)

def get_package_folder(name):
    return r"""
function out = get_package_folder()

%   GET_PACKAGE_FOLDER -- Get the path to the package folder "{0}".
%
%       OUT:
%           - `out` (char)

path_components = fileparts( which('{0}.util.get_package_folder') );

if ( ispc() )
    slash = '\';
else
    slash = '/';
end

path_components = strsplit( path_components, slash );
path_components = path_components(1:end-1);

out = strjoin( path_components, slash );

end""".format(name)

def close_ports(name):
	return r"""
function close_ports()

%	CLOSE_PORTS -- Close open serial ports.

ports = instrfind;
if ( isempty(ports) ), return; end;
fclose( ports );

end"""

def get_all():
	return {
		'print_error_stack': print_error_stack,
		'close_ports': close_ports,
    'get_package_folder': get_package_folder,
    'get_project_folder': get_project_folder,
    'add_depends': add_depends
	}