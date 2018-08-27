# task_maker

`task_maker` creates a barebones fixation task under a given namespace, which can then be modified and extended as necessary.

# dependencies

* [psychtoolbox](http://psychtoolbox.org/)
* [ptb_helpers](https://github.com/nfagan/ptb_helpers)
* [serial_comm](https://github.com/nfagan/serial_comm)

# example

```matlab
addpath( 'path/to/task_maker/repository/' );

task_name = 'eg';
%   note that the dependencies listed above will need to be on
%   matlab's search path for the task to run. If `task_path` points 
%   to a folder that also contains `ptb_helpers` and `serial_comm`, 
%   then those will be added automatically.
task_path = 'path/to/save/inside';

task_maker( task_name, task_path );

addpath( fullfile(task_path, task_name) );

%   `eg` must match `task_name`
eg.task.start();
```