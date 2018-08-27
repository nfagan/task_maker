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

% ID
conf.(const.config_id) = true;

% PATHS
PATHS = struct();
PATHS.repositories = fileparts( {0}.util.get_project_folder() );

% DEPENDENCIES
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
time_in.new_trial = 0;
time_in.fixation = 1;

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

% EXPORT
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

def diff(name):
  return r"""
function missing = diff(saved_conf, display)

%   DIFF -- Return missing fields in the saved config file.
%
%     missing = ... diff() compares the saved config file and the config
%     file that would be created by ... config.create(). Fields that are
%     present in the created config file but absent in the saved config
%     file are returned in `missing`. If no fields are missing, `missing`
%     is an empty cell array.
%
%     ... diff(), without an output argument, displays missing fields
%     in a human-readable way.
%
%     ... diff( conf ) uses the config file `conf` instead of the saved
%     config file.
%
%     ... diff( ..., false ) does not display missing fields.
%
%     IN:
%       - `saved_conf` (struct) |OPTIONAL|
%     OUT:
%       - `missing` (cell array of strings, {{}})

if ( nargin < 1 || isempty(saved_conf) )
  saved_conf = {0}.config.load();
else
  {0}.util.assertions.assert__is_config( saved_conf );
end
if ( nargin < 2 )
  if ( nargout == 0 )
    display = true;
  else
    display = false;
  end
else
  assert( isa(display, 'logical'), 'Display flag must be logical; was "%s".' ...
    , class(display) );
end

created_conf = {0}.config.create( false ); % false to not save conf

missing = get_missing( created_conf, saved_conf, '', 0, {{}}, display );

if ( ~display ), return; end
if ( isempty(missing) ), fprintf( '\nAll up-to-date.' ); end
fprintf( '\n' );

end

function missed = get_missing( created, saved, parent, ntabs, missed, display )

%   GET_MISSING -- Identify missing fields, recursively.

if ( ~isstruct(created) || ~isstruct(saved) ), return; end

created_fields = fieldnames( created );
saved_fields = fieldnames( saved );

missing = setdiff( created_fields, saved_fields );
shared = intersect( created_fields, saved_fields );

tabrep = @(x) repmat( '   ', 1, x );
join_func = @(x) sprintf( '%s.%s', parent, x );

if ( numel(missing) > 0 )
  if ( display )
    fprintf( '\n%s - %s', tabrep(ntabs), parent );
    cellfun( @(x) fprintf('\n%s - %s', tabrep(ntabs+1), x), missing, 'un', false );
  end
  missed(end+1:end+numel(missing)) = cellfun( join_func, missing, 'un', false );
end

for i = 1:numel(shared)
  created_ = created.(shared{{i}});
  saved_ = saved.(shared{{i}});
  child = join_func( shared{{i}} );
  missed = get_missing( created_, saved_, child, ntabs+1, missed, display );
end

end""".format(name)

def reconcile(name):
  return r"""
  function conf = reconcile(conf)

%   RECONCILE -- Add missing fields to config file.
%
%     conf = ... reconcile() loads the current config file and checks for
%     missing fields, that is, fields that are present in the config file
%     that would be generated by ... .config.create(), but which are not
%     present in the saved config file. Any missing fields are set to the
%     contents of the corresponding fields as defined in ...
%     .config.create().
%
%     conf = ... reconcile( conf ) uses the config file `conf`, instead of
%     the saved config file.
%
%     IN:
%       - `conf` (struct) |OPTIONAL|
%     OUT:
%       - `conf` (struct)

if ( nargin < 1 )
  conf = {0}.config.load(); 
end

display = false;
missing = {0}.config.diff( conf, display );

if ( isempty(missing) )
  return;
end

%   don't save
do_save = false;
created = {0}.config.create( do_save );

for i = 1:numel(missing)
  current = missing{{i}};
  eval( sprintf('conf%s = created%s;', current, current) );
end

end""".format(name)

def get_all():
	return {
		'create': create,
		'save': save,
		'load': load,
		'is_config': is_config,
		'constants': constants,
    'diff': diff,
    'reconcile': reconcile
	}