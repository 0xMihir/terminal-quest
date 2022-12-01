class Logger:
    def __init__(self):
        pass
        
        # self._log_file = None
        # self._app_name = None
        # self._force_flush = False
        # self._pid = os.getpid()

        # self._cached_log_level = None
        # self._cached_output_level = None
        # self._load_conf()

        # log = os.getenv(LOG_ENV)
        # if log is not None:
        #     self._cached_log_level = normalise_level(log)

        # output = os.getenv(OUTPUT_ENV)
        # if output is not None:
        #     self._cached_output_level = normalise_level(output)

        # force_flush = os.getenv(FORCE_FLUSH_ENV)
        # if force_flush is not None:
        #     self._force_flush = True

    def _load_conf(self):
        pass
        
        # conf = None
        # if os.path.exists(CONF_FILE):
        #     with open(CONF_FILE, "r") as f:
        #         conf = yaml.load(f)

        # if conf is None:
        #     conf = {}

        # if "log_level" not in conf:
        #     conf["log_level"] = "none"

        # if "output_level" not in conf:
        #     conf["output_level"] = "none"

        # if self._cached_log_level is None:
        #     self._cached_log_level = normalise_level(conf["log_level"])

        # if self._cached_output_level is None:
        #     self._cached_output_level = normalise_level(conf["output_level"])

    def get_log_level(self):
        pass
        
        # if self._cached_log_level is None:
        #     self._load_conf()

        # return self._cached_log_level

    def get_output_level(self):
        pass
        
        # if self._cached_output_level is None:
        #     self._load_conf()

        # return self._cached_output_level

    def force_log_level(self, level):
        pass
        
        # normalised = normalise_level(level)
        # if not self._cached_log_level or \
        #    LEVELS[self._cached_log_level] < LEVELS[normalised]:
        #     self._cached_log_level = normalised

    def force_debug_level(self, level):
        pass
        
        # normalised = normalise_level(level)
        # if not self._cached_output_level or \
        #    LEVELS[self._cached_output_level] < LEVELS[normalised]:
        #     self._cached_output_level = normalised

    def set_app_name(self, name):
        pass
        # self._app_name = os.path.basename(name.strip()).lower().replace(" ", "_")
        # if self._log_file is not None:
        #     self._log_file.close()
        #     self._log_file = None

    def set_force_flush(self):
        pass
        # self._force_flush = True

    def unset_force_flush(self):
        pass
        # self._force_flush = False

    def write(self, msg, force_flush=False, **kwargs):
        pass
        # lname = "info"
        # if "level" in kwargs:
        #     lname = normalise_level(kwargs["level"])

        # level = LEVELS[lname]
        # sys_log_level = LEVELS[self.get_log_level()]
        # sys_output_level = LEVELS[self.get_output_level()]

        # if level > 0 and (level <= sys_log_level or level <= sys_output_level):
        #     if self._app_name is None:
        #         try:
        #             self.set_app_name(sys.argv[0])
        #         except (AttributeError, IndexError):
        #             # argv is likely not accessible, use default value
        #             self.set_app_name('unknown-app')

        #     lines = msg.encode('utf8') if type(msg) == unicode else msg
        #     lines = lines.strip().split("\n")

        #     log = {}
        #     log["pid"] = self._pid
        #     log.update(kwargs)
        #     log["level"] = lname

        #     # if an exception object was ed in, add it to the log fields
        #     tbk = None
        #     if 'exception' in kwargs:
        #         import traceback
        #         tbk = traceback.format_exc()
        #         log['exception'] = unicode(kwargs['exception']).encode('utf8')
        #         log['traceback'] = tbk

        #     for line in lines:
        #         log["time"] = time.time()
        #         log["message"] = line

        #         if level <= sys_log_level:
        #             if self._log_file is None:
        #                 self._init_log_file()
        #             self._log_file.write("{}\n".format(json.dumps(log)))

        #             if self._force_flush or force_flush:
        #                 self.sync()

        #         if level <= sys_output_level:
        #             output_line = "{}[{}] {} {}\n".format(
        #                 self._app_name,
        #                 decorate_string_only_terminal(self._pid, "yellow"),
        #                 decorate_with_preset(log["level"], log["level"], True),
        #                 log["message"]
        #             )
        #             sys.stderr.write(output_line)

    def sync(self):
        pass
        # self.flush()

    def error(self, msg, **kwargs):
        pass
        # kwargs["level"] = "error"
        # self.write(msg, **kwargs)

    def debug(self, msg, **kwargs):
        pass
        # kwargs["level"] = "debug"
        # self.write(msg, **kwargs)

    def warn(self, msg, **kwargs):
        pass
        # kwargs["level"] = "warn"
        # self.write(msg, **kwargs)

    def info(self, msg, **kwargs):
        pass
        # kwargs["level"] = "info"
        # self.write(msg, **kwargs)

    def flush(self):
        pass
        # if self._log_file and not self._log_file.closed:
        #     self._log_file.flush()

        # sys.stderr.flush()

    def _init_log_file(self):
        pass
        # if self._log_file is not None:
        #     self._log_file.close()

        # if os.getuid() == 0 and not is_sudoed:
        #     logs_dir = SYSTEM_LOGS_DIR
        # else:
        #     logs_dir = USER_LOGS_DIR

        # if not os.path.exists(logs_dir):
        #     os.makedirs(logs_dir)

        #     # Fix permissions in case we need to create the dir with sudo
        #     if is_sudoed:
        #         uid = pwd.getpwnam(usr).pw_uid
        #         gid = grp.getgrnam(usr).gr_gid
        #         os.chown(logs_dir, uid, gid)

        # log_fn = "{}/{}.log".format(logs_dir, self._app_name)

        # # Fix permissions in case we need to create the file with sudo
        # if not os.path.isfile(log_fn) and is_sudoed:
        #     # touch
        #     with open(log_fn, 'a'):
        #         

        #     uid = pwd.getpwnam(usr).pw_uid
        #     gid = grp.getgrnam(usr).gr_gid
        #     os.chown(log_fn, uid, gid)

        # self._log_file = open("{}/{}.log".format(logs_dir, self._app_name), "a")


logger = Logger()

