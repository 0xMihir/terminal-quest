# file_operations.py
#
# Copyright (C) 2014-2018 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Utilities relating to file operations


import os
import re
import pwd
import getpass
import grp
import shutil
import json
import fcntl
import errno
import stat
import time
import tempfile
import io
# shell.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Utilities related to shell and running commands


import os
import sys
import signal
import subprocess


def restore_signals():
    signals = ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ')
    for sig in signals:
        if hasattr(signal, sig):
            signal.signal(getattr(signal, sig), signal.SIG_DFL)


def run_cmd(cmd, localised=False, unsudo=False):
    '''
    Executes cmd, returning stdout, stderr, return code
    if localised is False, LC_ALL will be set to "C"
    '''
    env = os.environ.copy()
    if not localised:
        env['LC_ALL'] = 'C'

    if unsudo and \
            'SUDO_USER' in os.environ and \
            os.environ['SUDO_USER'] != 'root':
        cmd = "sudo -u {} bash -c '{}' ".format(os.environ['SUDO_USER'], cmd)

    process = subprocess.Popen(cmd, shell=True, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               preexec_fn=restore_signals)

    stdout, stderr = process.communicate()
    returncode = process.returncode
    return stdout, stderr, returncode


def run_cmd_log(cmd, localised=False, unsudo=False):
    '''
    Wrapper against run_cmd but Kano Logging executuion and return code
    '''

    from kano.logging import logger

    out, err, rv = run_cmd(cmd, localised, unsudo)
    logger.info("Command: {}".format(cmd))

    if len(out.strip()) > 0:
        logger.info(out)

    if len(err.strip()) > 0:
        logger.error(err)

    logger.info("Return value: {}".format(rv))

    return out, err, rv


def run_bg(cmd, localised=False, unsudo=False):
    '''
    Starts cmd program in the background
    '''
    env = os.environ.copy()
    if not localised:
        env['LC_ALL'] = 'C'

    if unsudo and \
            'SUDO_USER' in os.environ and \
            os.environ['SUDO_USER'] != 'root':
        cmd = "sudo -u {} bash -c '{}' ".format(os.environ['SUDO_USER'], cmd)

    s = subprocess.Popen(cmd, shell=True, env=env)
    return s


def run_term_on_error(cmd, localised=False):
    o, e, rc = run_cmd(cmd, localised)
    if e:
        sys.exit(
            '\nCommand:\n{}\n\nterminated with error:\n{}'
            .format(cmd, e.strip())
        )
    return o, e, rc


def run_print_output_error(cmd, localised=False):
    o, e, rc = run_cmd(cmd, localised)
    if o or e:
        print('\ncommand: {}'.format(cmd))
    if o:
        print('output:\n{}'.format(o.strip()))
    if e:
        print('\nerror:\n{}'.format(e.strip()))
    return o, e, rc

def get_user_unsudoed():
    if 'SUDO_USER' in os.environ:
        return os.environ['SUDO_USER']
    elif 'LOGNAME' in os.environ:
        return os.environ['LOGNAME']
    else:
        return 'root'



def play_sound(path,background=False):
    pass
class TimeoutException(Exception):
    pass


def get_path_owner(path):
    owner = ''
    try:
        owner = pwd.getpwuid(os.stat(path).st_uid).pw_name
    except (IOError, OSError) as exc_err:
        from kano.logging import logger
        logger.warn(
            "Can't get path owner on {} due to permission/IO issues - {}"
            .format(path, exc_err)
        )

    return owner


def read_file_contents(path):
    if os.path.exists(path):
        with open(path) as infile:
            return infile.read().strip()


def write_file_contents(path, data):
    with open(path, 'w') as outfile:
        outfile.write(data)


def read_file_contents_as_lines(path):
    if os.path.exists(path):
        with open(path) as infile:
            content = infile.readlines()
            lines = [line.strip() for line in content]
            return lines


def delete_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def empty_directory(dir_path):
    """ This function removes all files and directories from a directory
    without deleting it.
    """
    if not os.path.exists(dir_path):
        from kano.logging import logger
        logger.warn("Can't empty, '{}' it doesn't exist".format(dir_path))
        return False

    if not os.path.isdir(dir_path):
        from kano.logging import logger
        logger.warn("Can't empty, '{}' it isn't a directory".format(dir_path))
        return False

    # If the current user is not the same as path owner we want to stop to
    # prevent silently introducing ownership issues
    if getpass.getuser() != get_path_owner(dir_path):
        from kano.logging import logger
        logger.warn(
            "Can't empty, '{}' owner is not as current user"
            .format(dir_path)
        )
        return False

    try:
        perm_mask = stat.S_IMODE(os.stat(dir_path).st_mode)
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path, mode=perm_mask)
    except (IOError, OSError) as exc_err:
        from kano.logging import logger
        logger.warn(
            "Can't empty, '{}' due to permission/IO issues - {}"
            .format(dir_path, exc_err)
        )
        return False

    return True


def recursively_copy(src, dst):
    src_dir = os.path.abspath(src)
    dest_dir = os.path.abspath(dst)

    if not os.path.isdir(src_dir) or not os.path.isdir(dest_dir):
        from kano.logging import logger
        logger.warn(
            "Can't copy '{}' contents into '{}', one of them is not a dir"
            .format(src_dir, dest_dir)
        )
        return False

    try:
        for root_d, dirs, files in os.walk(src_dir):
            # Firstly create the dirs
            dest_root = os.path.join(
                dest_dir,
                os.path.relpath(root_d, src_dir)
            )
            for dir_n in dirs:
                new_dir = os.path.join(dest_root, dir_n)
                os.mkdir(new_dir)
            # Now deal with the files
            for file_n in files:
                src_file = os.path.join(root_d, file_n)
                new_file = os.path.join(dest_root, file_n)
                shutil.copy(src_file, new_file)
    except (IOError, OSError) as exc_err:
        from kano.logging import logger
        logger.warn(
            "Can't copy '{}' contents into '{}', due to permission/IO - {}"
            .format(src_dir, dest_dir, exc_err)
        )
        return False
    return True


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def list_dir(dir_path):
    if os.path.exists(dir_path):
        return os.listdir(dir_path)

    return list()


def chown_path(path, user=None, group=None):
    user_unsudoed = get_user_unsudoed()
    if not user:
        user = user_unsudoed
    if not group:
        group = user_unsudoed
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(path, uid, gid)
    except KeyError as e:
        from kano.logging import logger
        logger.error(
            'user {} or group {} do not match with existing'.format(user, group))
        ret_val = False
    except OSError as e:
        from kano.logging import logger
        logger.error(
            'Error while trying to chown, root priviledges needed {}'.format(e))
        ret_val = False
    else:
        ret_val = True
    return ret_val


def read_json(filepath, silent=True):
    try:
        return json.loads(read_file_contents(filepath))
    except Exception:
        if not silent:
            raise


def write_json(filepath, data, prettyprint=False, sort_keys=True):
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=2, sort_keys=sort_keys)
    if prettyprint:
        _, _, rc = run_cmd('which underscore')
        if rc == 0:
            cmd = 'underscore print -i {filepath} -o {filepath}'.format(filepath=filepath)
            run_cmd(cmd)


def touch(path, times=None):
    """Set the access and modified times of the file specified by path.

    The function calls :func:`.ensure_dir` beforehand for you.
    This is essentially a simple wrapper for :func:`os.utime`.

    Args:
        path (str): Path to the file create/modify
        times (tuple): See :func:`os.utime`

    Returns:
        bool: Whether the operation was successful or not
    """
    try:
        ensure_dir(os.path.dirname(path))
        with open(path, 'a'):
            os.utime(path, times)

    except (IOError, OSError) as error:
        from kano.logging import logger
        logger.error(
            "Could not touch {} due to permission/IO - {}"
            .format(path, error)
        )
        return False
    return True


class open_locked(io.FileIO):
    """ A version of open with an exclusive lock to be used within
        controlled execution statements.
    """
    def __init__(self, *args, **kwargs):
        """
        pass optional nonblock=True for nonblocking behavior
        pass optional timeout=seconds for timeout blocking.
         If timeout is exhausted, we raise an exception
        """

        # we need to process 'nonblock' before calling
        # super().__init__ because that does not know about 'nonblock'
        mode = fcntl.LOCK_EX
        if kwargs.get('nonblock') is not None:
            mode = mode | fcntl.LOCK_NB
            del kwargs['nonblock']

        timeout = kwargs.get('timeout')
        if timeout is not None:
            mode = mode | fcntl.LOCK_NB
            del kwargs['timeout']

        super(open_locked, self).__init__(*args, **kwargs)

        def flock_try(self, mode):
            # Try locking a file
            # return True on success, "wait" if it is locked

            try:
                fcntl.flock(self, mode)
            except IOError as e:
                if e.errno == errno.EAGAIN:
                    return "wait"
                raise e
            return True

        if timeout:
            # Lock, or retry until timeout is exhausted
            now = time.clock()
            res = False
            while (time.clock() - now) < timeout:
                res = flock_try(self, mode)
                if res is True:
                    break
            if res is not True:
                raise TimeoutException()
        else:
            fcntl.flock(self, mode)


def sed(pattern, replacement, file_path, use_regexp=True):
    """ Search and replace a pattern in a file.

    The search happens line-by-line, multiline patterns won't work

    :param pattern: a regular expression to search for
    :param replacement: the replacement string
    :param file_path: location of the file to process
    :returns: number of lines changed
    :raises IOError: File doesn't exist
    """

    changed = 0

    with open(file_path, "r") as file_handle:
        lines = file_handle.readlines()

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_f:
        for line in lines:
            if use_regexp:
                modified_line = re.sub(pattern, replacement, line)
            else:
                modified_line = line.replace(pattern, replacement)

            tmp_f.write(modified_line)

            if line != modified_line:
                changed += 1

    shutil.move(tmp_f.name, file_path)

    return changed

# user.py
#
# Copyright (C) 2014-2018 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Utilities related to linux users


import os
import sys
import pwd
import getpass


def get_user_getpass():
    return getpass.getuser()


def get_user():
    return os.environ.get('LOGNAME', '')


def get_user_unsudoed():
    if 'SUDO_USER' in os.environ:
        return os.environ['SUDO_USER']
    elif 'LOGNAME' in os.environ:
        return os.environ['LOGNAME']
    else:
        return 'root'


def get_home():
    return os.path.expanduser('~')


def get_home_by_username(username):
    return pwd.getpwnam(username).pw_dir


def get_all_home_folders(root=False, skel=False):
    home = '/home'
    folders = [os.path.join(home, f) for f in os.listdir(home)]
    if root:
        folders += ['/root']
    if skel:
        folders += ['/etc/skel']
    return folders


def enforce_root(msg):
    if os.getuid() != 0:
        sys.stderr.write(msg.encode('utf-8') + "\n")
        sys.exit(1)