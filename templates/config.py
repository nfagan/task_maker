def create(name):
	return r"""
function conf = create(do_save)

%   CREATE -- Create the config file. 
%
%     Define editable properties of the config file here.
%
%     IN:
%       - `do_save` (logical) -- Indicate whether to save the created
%         config file. Default is `false`

if ( nargin < 1 ), do_save = false; end

const = {0}.config.constants();

conf = struct();

%   ID
conf.(const.config_id) = true;

%   PATHS
PATHS = struct();
PATHS.repositories = '';

%   DEPENDENCIES
DEPENDS = struct();
DEPENDS.repositories = {{ 'ptb_helpers', 'serial_comm' }};

%	INTERFACE
INTERFACE = struct();
INTERFACE.stop_key = KbName( 'escape' );
INTERFACE.use_mouse = true;
INTERFACE.use_reward = false;

%	SCREEN
SCREEN = struct();

SCREEN.full_size = get( 0, 'screensize' );
SCREEN.index = 0;
SCREEN.background_color = [ 0 0 0 ];
SCREEN.rect = [ 0, 0, 400, 400 ];

%	TIMINGS
TIMINGS = struct();

time_in = struct();
time_in.fixation = 0.1;

TIMINGS.time_in = time_in;

%	STIMULI
STIMULI = struct();
STIMULI.setup = struct();

non_editable_properties = {{{{ 'placement', 'has_target', 'image_matrix' }}}};

STIMULI.setup.fix_square = struct( ...
    'class',            'Rectangle' ...
  , 'size',             [ 50, 50 ] ...
  , 'color',            [ 255, 255, 255 ] ...
  , 'placement',        'center' ...
  , 'has_target',       true ...
  , 'target_duration',  0.3 ...
  , 'target_padding',   50 ...
  , 'non_editable',     non_editable_properties ...
);

%	SERIAL
SERIAL = struct();
SERIAL.port = 'COM3';
SERIAL.channels = {{ 'A' }};

%   EXPORT
conf.PATHS = PATHS;
conf.DEPENDS = DEPENDS;
conf.TIMINGS = TIMINGS;
conf.STIMULI = STIMULI;
conf.SCREEN = SCREEN;
conf.INTERFACE = INTERFACE;
conf.SERIAL = SERIAL;

if ( do_save )
  {0}.config.save( conf );
end

end""".format(name)

def save(name):
	return r"""
function save(conf)

%   SAVE -- Save the config file.

{0}.util.assertions.assert__is_config( conf );
const = {0}.config.constants();
fprintf( '\n Config file saved\n\n' );
save( fullfile(const.config_folder, const.config_filename), 'conf' );

end""".format(name)

def load(name):
	return r"""
function conf = load()

%   LOAD -- Load the config file.

const = {0}.config.constants();

config_folder = const.config_folder;
config_file = const.config_filename;

config_filepath = fullfile( config_folder, config_file );

if ( exist(config_filepath, 'file') ~= 2 )
  fprintf( '\n Creating config file ...' );
  conf = {0}.config.create();
  {0}.config.save( conf );
end

conf = load( config_filepath );
conf = conf.(char(fieldnames(conf)));

try
  {0}.util.assertions.assert__is_config( conf );
catch err
  fprintf( ['\n Could not load the config file saved at ''%s'' because ' ...
    , ' it is not recognized as a valid config file.\n\n'], config_filepath );
  throwAsCaller( err );
end

end""".format(name)

def is_config(name):
	return r"""
function out = is_config(conf)

%   IS_CONFIG -- Check if a variable is a config file.

out = true;

if ( ~isa(conf, 'struct') )
  out = false;
  return;
end

const = {0}.config.constants();

if ( ~isfield(conf, const.config_id) )
  out = false;
end

end""".format(name)

def constants(name):
	return r"""
function const = constants()

%   CONSTANTS -- Get constants used to define the config file structure.

const = struct();

config_folder = fileparts( which(sprintf('{0}.config.%s', mfilename)) );

const.config_filename = 'config.mat';
const.config_id = '{0}__IS_CONFIG__';
const.config_folder = config_folder;

end""".format(name)

def get_all():
	return {
		'create': create,
		'save': save,
		'load': load,
		'is_config': is_config,
		'constants': constants
	}