addpath( fullfile(pathfor('repositories'), 'task_maker') );

%%

[status, result] = task_maker.make( 'cs_plus', cd );

disp( status );
disp( result );

%%

addpath( './cs_plus' );
addpath( genpath(fullfile(pathfor('repositories'), 'ptb_helpers')) );

%%

cs_plus.config.create( true );
cs_plus.util.add_depends
cs_plus.task.start()