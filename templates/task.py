def start(name):
	return r"""
function err = start()

%   START -- Attempt to setup and run the task.
%
%     OUT:
%       - `err` (double, MException) -- 0 if successful; otherwise, the
%         raised MException, if setup / run fails.

try
  opts = {0}.task.setup();
catch err
  {0}.task.cleanup();
  {0}.util.print_error_stack( err );
  return;
end

try
  err = 0;
  {0}.task.run( opts );
  {0}.task.cleanup();
catch err
  {0}.task.cleanup();
  {0}.util.print_error_stack( err );
end

end""".format(name)

def setup(name):
	return r"""
function opts = setup()

%   SETUP -- Prepare to run the task based on the saved config file.
%
%     Opens windows, starts EyeTracker, initializes Arduino, etc.
%
%     OUT:
%       - `opts` (struct) -- Config file, with additional parameters
%         appended.

opts = {0}.config.load();

STIMULI = opts.STIMULI;
SCREEN = opts.SCREEN;
SERIAL = opts.SERIAL;

%   SCREEN
[windex, wrect] = Screen( 'OpenWindow', SCREEN.index, SCREEN.background_color, SCREEN.rect );

%   WINDOW
WINDOW.center = round( [mean(wrect([1 3])), mean(wrect([2 4]))] );
WINDOW.index = windex;
WINDOW.rect = wrect;

%   TRACKER
TRACKER = EyeTracker( '', cd, WINDOW.index );
TRACKER.bypass = opts.INTERFACE.use_mouse;
TRACKER.init();

%   STIMULI
stim_fs = fieldnames( STIMULI.setup );
for i = 1:numel(stim_fs)
  stim = STIMULI.setup.(stim_fs{{i}});
  if ( ~isstruct(stim) ), continue; end;
  if ( ~isfield(stim, 'class') ), continue; end
  switch ( stim.class )
    case 'Rectangle'
      stim_ = Rectangle( windex, wrect, stim.size );
    case 'Image'
      im = stim.image_matrix;
      stim_ = Image( windex, wrect, stim.size, im );
  end
  stim_.color = stim.color;
  stim_.put( stim.placement );
  if ( stim.has_target )
    duration = stim.target_duration;
    padding = stim.target_padding;
    stim_.make_target( TRACKER, duration );
    stim_.targets{{1}}.padding = padding;
  end
  STIMULI.(stim_fs{{i}}) = stim_;
end

%   SERIAL
comm = serial_comm.SerialManager( SERIAL.port, struct(), SERIAL.channels );
comm.bypass = ~opts.INTERFACE.use_reward;
comm.start();
SERIAL.comm = comm;

%   EXPORT
opts.STIMULI = STIMULI;
opts.WINDOW = WINDOW;
opts.TRACKER = TRACKER;
opts.SERIAL = SERIAL;

end""".format(name)

def run(name):
	return r"""
function run(opts)

%   RUN -- Run the task based on the saved config file options.
%
%     IN:
%       - `opts` (struct)

INTERFACE = opts.INTERFACE;

while ( true )

  [key_pressed, ~, key_code] = KbCheck();

  if ( key_pressed )
    if ( key_code(INTERFACE.stop_key) ), break; end
  end

end

end
	""".format(name)

def cleanup(name):
    return r"""
function cleanup(tracker)

%   CLEANUP -- Close open files, ports, etc.

sca;

ListenChar( 0 );

{0}.util.close_ports();

if ( nargin >= 1 && ~isempty(tracker) )
  tracker.shutdown()
end

end""".format(name)

def get_all():
	return {
		'start': start,
		'setup': setup,
    'cleanup': cleanup,
    'run': run
	}