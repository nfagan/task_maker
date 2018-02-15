function [status, result] = make(name, pathstr)

%   MAKE -- Create a task template.
%
%     IN:
%       - `name` (char) -- Name of the task.
%       - `path` (char) -- Path to the outer folder in which to create the
%         task structure.
%     OUT:
%       - `status` (number)
%       - `result` (number)

assert( ischar(name) && ischar(pathstr), 'Specify "name" and "path" as strings.' );

if ( ispc() )
  slash = '\'; 
else
  slash = '/';
end

m_path = fileparts( which('task_maker.make') );
m_path_components = strsplit( m_path, slash );

py_script_path = strjoin( m_path_components(1:end-1), slash );

py_script = fullfile( py_script_path, 'task_maker.py' );

cmd = sprintf( 'python "%s" --name "%s" --path "%s"', py_script, name, pathstr );

[status, result] = system( cmd );

end