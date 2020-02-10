#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: mattermost_config

short_description: Set Mattermost config

version_added: "2.9.4"

description:
    - "Idempotently set Mattermost config values"

options:
    key:
        description:
            - Mattermost config key
        required: true
    value:
        description:
            - Mattermost config value
        required: true
    mattermost_path:
        description:
            - mattermost command location
        default: /opt/mattermost/bin/mattermost
        required: false

author:
    - Jeremy Maness <jwmanes2@ncsu.edu>
'''

EXAMPLES = '''
# Change site URL
- name: Change site URL
  mattermost_config:
    key: ServiceSettings.SiteURL
    value: mattermost.example.com
'''

RETURN = '''
key:
    description: The output message that the test module generates
    type: str
    returned: success
original_value:
    description: The original value associated to the Mattermost config key
    type: str
    returned: success
new_value:
    description: The new value assigned to the Mattermost config key
    type: str
    returned: changed
'''

from ansible.module_utils.basic import AnsibleModule
from distutils import util
import shlex
from subprocess import Popen, PIPE
import re

def runcmd(cmd):
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err

def run_module():
    module_args = dict(
        key=dict(type='str', required=True),
        value=dict(type='str', required=True),
        mattermost_path=dict(type='str', required=False, default="/opt/mattermost/bin/mattermost")
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    try:
        get_exitcode, out, _ = runcmd("{} config get {}".format(
            module.params['mattermost_path'],
            module.params['key']))

        if get_exitcode != 0:
            raise Exception('Unable to find setting {}'.format(module.params['key']))
        else:
            current_setting = out.decode("utf-8")
            z = re.match("{}: \"(.*)\"".format(module.params['key']), current_setting)
            if z:
                current_value = z.group(1)
                result['key'] = module.params['key']
                result['original_value'] = current_value

                if (current_value != module.params['value'] and not compareIfBool(current_value, module.params['value'])):
                    set_exitcode, _, _ = runcmd("{} config set {} {}".format(
                        module.params['mattermost_path'],
                        module.params['key'],
                        module.params['value']))

                    if set_exitcode == 0:
                        result['changed'] = True
                        result['new_value'] = module.params['value']
                    else:
                        result['message'] = current_value
            else:
                raise Exception('Unable to parse current setting {}'.format(current_setting))

    except Exception as err:
        module.fail_json(msg=err.args[0], **result)

    module.exit_json(**result)

def compareIfBool(val1, val2):
    try:
        return util.strtobool(val1) == util.strtobool(val2)
    except ValueError:
        return False

def main():
    run_module()

if __name__ == '__main__':
    main()
