__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module = AnsibleModule(
        argument_spec = dict(
            cluster = dict(type = 'str'),
            context = dict(type = 'str'),
            endpoints = dict(type = 'list', elements = 'str'),
            nodes = dict(type = 'list', elements = 'str', required = True),
            talosconfig = dict(type = 'path'),
        ),
        supports_check_mode = True,
    )

    result = dict(
        changed = False,
        message = ''
    )

    cluster = module.params['cluster']
    context = module.params['context']
    endpoints = module.params['endpoints']
    nodes = module.params['nodes']
    talosconfig = module.params['talosconfig']

    cmd = ["talosctl", "bootstrap"]

    if cluster:
        cmd.append("-c")
        cmd.append(cluster)

    if context:
        cmd.append("--context")
        cmd.append(context)

    for item in endpoints or []:
        cmd.append("-e")
        cmd.append(item)

    for item in nodes:
        cmd.append("-n")
        cmd.append(item)
    
    if talosconfig:
        cmd.append("--talosconfig")
        cmd.append(talosconfig)
    
    rc, stdout, stderr = module.run_command(cmd)

    if rc == 0:
        module.exit_json(**result)
    else:
        module.fail_json(msg = stderr, **result)

def main():
    run_module()


if __name__ == '__main__':
    main()