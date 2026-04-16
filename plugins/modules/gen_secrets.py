#!/usr/bin/python
# -*- coding: utf-8 -*-
__metaclass__ = type

DOCUMENTATION = '''
---
module: gen_secrets
short_description: Generates a secrets bundle file which can later be used to generate a config
description:
    - Generates a secrets bundle file which can later be used to generate a config.
options:
    force:
        description:
            - overwrite existing file
        type: bool
    output_file:
        description:
            - path of the output file (default "secrets.yaml")
        type: path
    talos_version:
        description:
            - the desired Talos version to generate secrets bundle for (backwards compatibility, e.g. v0.8)
        type: str

version_added: 0.2.0
'''


from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module = AnsibleModule(
        argument_spec = dict(
            force = dict(type = 'bool'),
            output_file = dict(type = 'path'),
            output_type = dict(type = 'str', choices = ['file', 'stdout'], default = 'file'),
            talos_version = dict(type = 'str')
        ),
        supports_check_mode = True,
    )

    result = dict(
        changed = False,
        message = ''
    )

    force = module.params['force']
    output_file = module.params['output_file']
    output_type = module.params['output_type']
    talos_version = module.params['talos_version']

    cmd = ["talosctl", "gen", "secrets"]

    if output_type == 'file':
        if output_file:
            cmd.append("-o")
            cmd.append(output_file)
            if force:
                cmd.append("-f")
    else:
        cmd.append("-")
        result['changed'] = True

    if talos_version:
        cmd.append("--talos-version")
        cmd.append(talos_version)
    
    if os.path.exists:
        rc, stdout, stderr = module.run_command(cmd)
    else:
        module.exit_json(**result)

    if rc == 0:
        module.exit_json(**result)
    else:
        module.fail_json(msg = stderr, **result)

def main():
    run_module()


if __name__ == '__main__':
    main()