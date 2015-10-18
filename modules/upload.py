#!/usr/bin/env python
# coding=utf-8
import ansible.runner
import json
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

print upload_directory("/root/upload.py","/tmp/","127.0.0.1")
