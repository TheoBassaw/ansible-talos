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
    encrypt:
        description:
            - encrypt the secrets with sops. Must have SOPS installed (https://github.com/getsops/sops)
        type: bool
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

def run_module():
    module = AnsibleModule(
        argument_spec = dict(
            encrypt = dict(type = 'bool'),
            force = dict(type = 'bool'),
            output_file = dict(type = 'path'),
            talos_version = dict(type = 'str')
        ),
        supports_check_mode=True,
    )

    result = dict(
        changed = False,
        message = ''
    )

    encrypt = module.params['encrypt']
    force = module.params['force']
    output_file = module.params['output_file']
    talos_version = module.params['talos_version']

    cmd = ["talosctl", "gen", "secrets", "-o", "-"]



    if rc_diff == 0 and "No changes." not in stderr_diff:
        result['changed'] = True

    rc, stdout, stderr = module.run_command(cmd)

    if rc== 0:
        module.exit_json(**result)
    else:
        module.fail_json(msg = stderr, **result)

def main():
    run_module()


if __name__ == '__main__':
    main()