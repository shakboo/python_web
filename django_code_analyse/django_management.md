# Django Management

标签：django

[TOC]

## 前言
>Django框架的整个数据流向，服务启动，端口监听等基础核心功能都是按照WSGI标准进行开发的。

## 启动流程
>当Django服务启动时，最先执行的是项目中的manage.py
```python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TestDrivenDjango.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        ...

    execute_from_command_line(sys.argv)

```
>当`from django.core.management import execute_from_command_line`这段代码执行的时候，会先将`django.core.management.__init__.py`中的`execute_from_command_line`函数导入到当前程序的命名空间中
```python
def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
```
>`execute_from_command_line`是一个工厂函数，负责调用ManagementUtility类利用excute方法来解析参数和启动wsgi服务，通过manage.py调用的参数全部存放在django\core\management\commands

## ManagementUtility
```python
class ManagementUtility(object):
    """
    Encapsulates the logic of the django-admin and manage.py utilities.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None
        
    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('--settings')
        parser.add_argument('--pythonpath')
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
        except CommandError:
            pass  # Ignore any option errors at this point.

        try:
            settings.INSTALLED_APPS
        except ImproperlyConfigured as exc:
            self.settings_exception = exc

        if settings.configured:
            # Start the auto-reloading dev server even if the code is broken.
            # The hardcoded condition is a code smell but we can't rely on a
            # flag on the command class because we haven't located it yet.
            if subcommand == 'runserver' and '--noreload' not in self.argv:
                try:
                    autoreload.check_errors(django.setup)()
                except Exception:
                    # The exception will be raised later in the child process
                    # started by the autoreloader. Pretend it didn't happen by
                    # loading an empty list of applications.
                    apps.all_models = defaultdict(OrderedDict)
                    apps.app_configs = OrderedDict()
                    apps.apps_ready = apps.models_ready = apps.ready = True

                    # Remove options not compatible with the built-in runserver
                    # (e.g. options for the contrib.staticfiles' runserver).
                    # Changes here require manually testing as described in
                    # #27522.
                    _parser = self.fetch_command('runserver').create_parser('django', 'runserver')
                    _options, _args = _parser.parse_known_args(self.argv[2:])
                    for _arg in _args:
                        self.argv.remove(_arg)

            # In all other cases, django.setup() is required to succeed.
            else:
                django.setup()

        self.autocomplete()

        if subcommand == 'help':
            if '--commands' in args:
                sys.stdout.write(self.main_help_text(commands_only=True) + '\n')
            elif len(options.args) < 1:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        # Special-cases: We want 'django-admin --version' and
        # 'django-admin --help' to work, for backwards compatibility.
        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            sys.stdout.write(django.get_version() + '\n')
        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)
```
>execute函数的重点在于`self.fetch_command(subcommand).run_from_argv(self.argv)`

### fentch_command
```python
    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "django-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            if os.environ.get('DJANGO_SETTINGS_MODULE'):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                settings.INSTALLED_APPS
            else:
                sys.stderr.write("No Django settings specified.\n")
            sys.stderr.write(
                "Unknown command: %r\nType '%s help' for usage.\n"
                % (subcommand, self.prog_name)
            )
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass
```
>该函数利用django内置的命令管理工具去匹配具体的模块，比如`self.fetch_command('runserver')`最终找到`django.contrib.staticfiles.management.commands.runserver.Command`。
django中的命令工具代码组织采用的是策略模式+接口模式，也就是说`django.core.management.commands`这个目录下面存在各种命令工具，每个工具下面都有一个Command接口，当匹配到'runserver'时调用'runserver'命令工具的Command接口，当匹配到'migrate'时调用'migrate'命令工具的Command接口。

### Command
```python
# django/contrib/staticfiles/management/commands/runserver.py
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management.commands.runserver import \
    Command as RunserverCommand


class Command(RunserverCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--nostatic', action="store_false", dest='use_static_handler', default=True,
            help='Tells Django to NOT automatically serve static files at STATIC_URL.',
        )
        parser.add_argument(
            '--insecure', action="store_true", dest='insecure_serving', default=False,
            help='Allows serving static files even if DEBUG is False.',
        )

    def get_handler(self, *args, **options):
        handler = super(Command, self).get_handler(*args, **options)
        use_static_handler = options['use_static_handler']
        insecure_serving = options['insecure_serving']
        if use_static_handler and (settings.DEBUG or insecure_serving):
            return StaticFilesHandler(handler)
        return handler
```
```python
# django.contrib.staticfiles.management.commands.runserver.Command
from django.core.servers.basehttp import get_internal_wsgi_application, run

class Command(BaseCommand):
    
    def execute(self, *args, **options):
        if options['no_color']:
            os.environ[str("DJANGO_COLORS")] = str("nocolor")
        super(Command, self).execute(*args, **options)    

    def get_handler(self, *args, **options):
        return get_internal_wsgi_application()
        
    def handle(self, *args, **options):
        ...
        self.run(**options)
        
    def run(self, **options):
        use_reloader = options['use_reloader']

        if use_reloader:
            autoreload.main(self.inner_run, None, options)
        else:
            self.inner_run(None, **options)        
            
    def inner_run(self, *args, **options):
        ...
        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler,
                ipv6=self.use_ipv6, threading=threading)
        except socket.error as e:
            ...
```
>上述两段代码中，第一个Command类继承了第二个Command类，这里需要注意的是get_handle函数，由于请求入口是第一个Command，所以需要注意第一个Command中的get_handle函数
>Command类继承了`django.core.management.base.BaseCommand`，因此实际上有很多可用的方法，而run_from_argv就是这个类的方法。
