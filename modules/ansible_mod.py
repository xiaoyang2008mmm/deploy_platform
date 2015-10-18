#!/usr/bin/python
# -*- coding: utf-8 -*- 
from ansible  import inventory
import ansible.runner
import json
def get_host_list(pattern="all"):
    h = inventory.Inventory()   
    group = h.list_groups() 
    list_host =  h.list_hosts(pattern = pattern)
    group +=list_host
    return group


def upload_directory(src_dir,dest_dir,host):
    runner = ansible.runner.Runner(
           module_name='copy',
           module_args='src=%s dest=%s  force=yes'%(src_dir,dest_dir),
           pattern= host,
           forks=10
        )
    datastructure = runner.run()
    data = json.dumps(datastructure,indent=4)
    return  data

#print upload_directory("/root/upload.py","/tmp/","127.0.0.1")


def git_clone(repo,dest_dir,host):
    runner = ansible.runner.Runner(
           module_name='git',
           module_args='repo=%s  clone=yes dest=%s'%(repo,dest_dir),
           pattern= host,
           forks=10
        )
    datastructure = runner.run()
    data = json.dumps(datastructure,indent=4)
    return  data

#print git_clone("https://github.com/xiaoyang2008mmm/deploy_platform.git","/data/workspaces/ssssssssss/","127.0.0.1")


def shell_scripts(script,host):
    runner = ansible.runner.Runner(
           module_name='script',
           module_args='%s'%script,
           pattern= host,
           forks=10
        )
    datastructure = runner.run()
    data = json.dumps(datastructure,indent=4)
    return  data


#print shell_scripts("/root/deploy_platform/tmp/after.sh","127.0.0.1")
