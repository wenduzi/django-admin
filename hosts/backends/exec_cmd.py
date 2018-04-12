import os
import sys
import multiprocessing
import paramiko
import django
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

BASE_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2])
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_site.settings")

django.setup()
from hosts import models


def by_paramiko(task_id):
    try:
        task_obj = models.TaskLog.objects.get(id=task_id)
        hosts = task_obj.hosts.select_related()
        cmd_text = task_obj.cmd_text
        pool = multiprocessing.Pool(processes=5)
        for host in hosts:
            pool.apply_async(paramiko_ssh, args=(host, cmd_text))
        pool.close()
        pool.join()
        set_task_summary(task_id)

    except ObjectDoesNotExist as e:
        sys.exit(e)


def set_task_summary(task_id):
    task_obj = models.TaskLog.objects.get(id=task_id)
    taskdetail_obj = models.TaskLogDetail.objects.filter(child_of_task=task_id)
    child_task_result = []
    for taskdetail in taskdetail_obj:
        child_task_result.append(taskdetail.result)

    if 'unknown' in child_task_result:
        task_result = 'unkown'
    elif 'failed' in child_task_result:
        task_result = 'faild'
    else:
        task_result = 'success'

    obj = models.TaskSummary(
        user=task_obj.user,
        task_id=task_obj,
        start_time=task_obj.start_time,
        end_time=timezone.now(),
        cmd_text=task_obj.cmd_text,
        task_result=task_result,
    )
    obj.save()


def paramiko_ssh(host, cmd_text):
    print('going to run %s on %s' % (cmd_text, host))
    bind_host = host
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host_user = bind_host.host_user.select_related().get()
    try:
        if host_user.auth_type == 'ssh-password':
            s.connect(bind_host.host.ip_address,
                      int(bind_host.host.port),
                      host_user.username,
                      host_user.password,
                      timeout=5)
        else:  # rsa_key
            pass
            '''
            key = paramiko.RSAKey.from_private_key_file(settings.RSA_PRIVATE_KEY_FILE)
            s.connect(bind_host.host.ip_addr,
                      int(bind_host.host.port),
                      bind_host.host_user.username,
                      pkey=key,
                      timeout=5)
            '''
        stdin, stdout, stderr = s.exec_command(cmd_text)
        result = stdout.read(), stderr.read()
        cmd_result = list(filter(lambda x: len(x) > 0, result))[0]
        result = 'success'

    except Exception as e:
        print("\033[31;1m%s\033[0m" % e)
        cmd_result = e
        result = 'failed'

    # for line in cmd_result:
    #    print line,

    # save output into db

    logdetail_obj = models.TaskLogDetail.objects.get(child_of_task_id=task_id, bind_host_id=bind_host.id)
    logdetail_obj.event_log = cmd_result
    logdetail_obj.date = timezone.now()
    logdetail_obj.result = result
    logdetail_obj.save()


def by_ansible(task_id):
    print('going to run %s' % task_id)


if __name__ == '__main__':
    required_args = ['-task_id', '-run_type']
    for arg in required_args:
        if arg not in sys.argv:
            sys.exit('arg[%s] is required' % arg)
    if len(sys.argv) < 5:
        sys.exit('5 aruguments is required but given %s' % len(sys.argv))

    task_id = sys.argv[sys.argv.index('-task_id') + 1]
    run_type = sys.argv[sys.argv.index('-run_type') + 1]

    if hasattr(__import__(__name__), run_type):
        func = getattr(__import__(__name__), run_type)
        func(task_id)
    else:
        sys.exit('Invalid run_type,support [by_paramiko] and [by_ansible]')
