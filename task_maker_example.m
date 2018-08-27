function task_maker_example(task_path, task_name)

%   TASK_MAKER_EXAMPLE -- Create example task.
%
%     task_maker_example() creates a task called 'example_task' in the
%     current directory, throwing an error if the task already exists.
%
%     task_maker_example( FOLDER ) creates 'example_task' in `FOLDER`,
%     instead of the current directory. If `FOLDER` is empty, the current
%     directory is used.
%
%     task_maker_example( ..., NAME ) creates `NAME` instead of
%     'example_task'.
%
%     See also task_maker.make
%
%     IN:
%       - `task_path` (char) |OPTIONAL|
%       - `task_name` (char) |OPTIONAL|

if ( nargin < 1 || isempty(task_path) ), task_path = cd; end
if ( nargin < 2 || isempty(task_name) ), task_name = 'example_task'; end

check_task_path( task_path, task_name );

[status, result] = task_maker.make( task_name, task_path );

disp( status );
disp( result );

end

function check_task_path(task_path, task_name)
if ( exist(fullfile(task_path, task_name), 'dir') == 7 )
  error( ['Cannot create "%s" because it already exists.' ...
    , ' Delete it first, or change `task_path` to a different directory.'], task_name )
end
end