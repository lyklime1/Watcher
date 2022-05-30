import time
import shutil
import os


class Watch:

    @staticmethod
    def start():
        shutil.rmtree(path_repl)
        os.mkdir(path_repl)
        for f in os.listdir(path_temp):
            if os.path.isdir(os.path.join(path_temp, f)):
                shutil.copytree(os.path.join(path_temp, f), os.path.join(path_repl, f))
            else:
                shutil.copyfile(os.path.join(path_temp, f), os.path.join(path_repl, f))
        if os.path.exists(path_log):
            os.remove(path_log)
        Watch.pars_dir(path_temp)
        time.sleep(interval)

    @staticmethod
    def check_del(path):
        for file in temp[path]:
            if os.path.isdir(file):
                Watch.check_del(file)
            elif not os.path.exists(file):
                Watch.log(file, 'deleted')
                Watch.delete(file)
                Watch.pars_dir(path)

    @staticmethod
    def check_changes(path):
        for name in os.listdir(path):
            file = os.path.join(path, name)
            if not os.path.isdir(file):
                if time.time() - os.path.getctime(file) <= interval:
                    Watch.log(file, 'created')
                    Watch.copy(file)
                    Watch.pars_dir(path)
                elif time.time() - os.stat(file).st_mtime <= interval:
                    Watch.log(file, 'modified')
                    Watch.copy(file)
            else:
                Watch.check_changes(file)

    @staticmethod
    def copy(path):
        shutil.copyfile(path, os.path.join(path_repl, os.path.basename(path)))

    @staticmethod
    def delete(file):
        if os.path.exists(file):
            os.remove(file)

    @staticmethod
    def log(file, ch_type):
        string = f"{file} {ch_type} {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n"
        if os.path.exists(path_log):
            with open(path_log, 'a') as log_f:
                print(string)
                log_f.write(string)
        else:
            with open(path_log, 'w') as log_f:
                print(string)
                log_f.write(string)

    @staticmethod
    def pars_dir(path):
        temp[path] = []
        for name in os.listdir(path):
            file = os.path.join(path, name)
            if not os.path.isdir(file):
                temp[path].append(file)
            else:
                Watch.pars_dir(file)


class Filtering:

    @staticmethod
    def path(text=''):
        while True:
            path = input(text)
            if os.path.exists(path):
                return path
            else:
                print('Path is not exist\n')

    @staticmethod
    def interval(text=''):
        while True:
            val = input(text)
            try:
                return int(val)
            except ValueError:
                print('Entered value is not integer\n')

    @staticmethod
    def check_paths():
        global path_repl, path_temp, path_log
        while path_temp == path_repl:
            print('Directory-source and directory-replica cannot be the same\n')
            path_temp = Filtering.path('Enter path to directory-source:\n')
            path_repl = Filtering.path('Enter path to directory-replica:\n')
        while path_temp == path_log or path_repl == path_log:
            print('Directory-source and directory-replica cannot contain a log file.\n')
            path_log = os.path.join(Filtering.path('Enter path to the directory to creating a log-file:\n'), 'log.txt')


if __name__ == '__main__':
    temp = {}
    path_temp = Filtering.path('Enter absolute path to directory-temlpate:\n')
    path_repl = Filtering.path('Enter absolute path to directory-replica:\n')
    interval = Filtering.interval('Enter synchronisation interval in seconds:\n')
    path_log = os.path.join(Filtering.path('Enter absolute path to directory for log-file:\n'), 'log.txt')
    Watch.start()
    while True:
        Watch.check_del(path_temp)
        Watch.check_changes(path_temp)
        time.sleep(interval)
