#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

DOCUMENTATION = '''
---
module: apply_config
short_description: Apply a new configuration to a node
description:
    - Apply a new configuration to a node.
options:
    cert_fingerprint:
        description:
            - list of server certificate fingeprints to accept
        type: list
        element: str
    cluster:
        description:
            - Cluster to connect to if a proxy endpoint is used.
        type: str
    config_patch:
        description:
            - the list of config patches to apply to the local config file before sending it to the node
        type: list
        element: path
    context:
        description:
            - Context to be used in command
        type: str
    endpoints:
        description:
            - override default endpoints in Talos configuration
        type: list
        element: str
    file:
        description:
            - the filename of the updated configuration
        type: path
        required: true
    insecure:
        description:
            - apply the config using the insecure (encrypted with no auth) maintenance service
        type: bool
    mode:
        description:
            - apply config mode
        type: str
        choices:
            - auto
            - no-reboot
            - reboot
            - staged
            - try
    nodes:
        description:
            - target the specified nodes
        type: list
        element: str
        required: true
    talosconfig:
        description:
            - The path to the Talos configuration file. Defaults to 'TALOSCONFIG' env variable if set, otherwise '$HOME/.talos/config' and '/var/run/secrets/talos.dev/config' in order.
        type: str
    timeout:
        description:
            - the config will be rolled back after specified timeout (if try mode is selected)
        type: str

version_added: 0.1.0
'''


from ansible.module_utils.basic import AnsibleModule

def run_module():
    module = AnsibleModule(
        argument_spec = dict(
            cert_fingerprint = dict(type = 'list', elements = 'str'),
            cluster = dict(type = 'str'),
            config_patch = dict(type = 'list', elements = 'path'),
            context = dict(type = 'str'),
            endpoints = dict(type = 'list', elements = 'str'),
            file = dict(type = 'path', required = True),
            insecure = dict(type = 'bool'),
            mode = dict(type = 'str', choices = ['auto', 'no-reboot', 'reboot', 'staged', 'try']),
            nodes = dict(type = 'list', elements = 'str', required = True),
            talosconfig = dict(type = 'path'),
            timeout = dict(type = 'str')
        ),
        supports_check_mode = True,
    )

    result = dict(
        changed = False,
        message = ''
    )

    cert_fingerprint = module.params['cert_fingerprint']
    cluster = module.params['cluster']
    config_patch = module.params['config_patch']
    context = module.params['context']
    endpoints = module.params['endpoints']
    file = module.params['file']
    insecure = module.params['insecure']
    mode = module.params['mode']
    nodes = module.params['nodes']
    talosconfig = module.params['talosconfig']
    timeout = module.params['timeout']

    cmd = ["talosctl", "apply-config", "-f", file]

    for item in cert_fingerprint or []:
        cmd.append("--cert-fingerprint")
        cmd.append(item)
    
    if cluster:
        cmd.append("-c")
        cmd.append(cluster)

    for item in config_patch or []:
        cmd.append("-p")
        cmd.append("@" + item)

    if context:
        cmd.append("--context")
        cmd.append(context)

    for item in endpoints or []:
        cmd.append("-e")
        cmd.append(item)

    if insecure:
        cmd.append("-i")
    
    if mode:
        cmd.append("-m")
        cmd.append(mode)

    for item in nodes:
        cmd.append("-n")
        cmd.append(item)
    
    if talosconfig:
        cmd.append("--talosconfig")
        cmd.append(talosconfig)

    if timeout:
        cmd.append("--timeout")
        cmd.append(timeout)

    if module.check_mode:
        module.exit_json(**result)

    if timeout and mode != 'try':
        module.fail_json(msg="timeout can only be used with mode=try")
    
    cmd_diff = cmd.copy()
    cmd_diff.append("--dry-run")

    rc_diff, stdout_diff, stderr_diff = module.run_command(cmd_diff)

    if rc_diff == 0 and "No changes." not in stderr_diff:
        result['changed'] = True

    rc, stdout, stderr = module.run_command(cmd)

    if rc == 0:
        module.exit_json(**result)
    else:
        module.fail_json(msg = stderr, **result)

def main():
    run_module()

if __name__ == '__main__':
    main()