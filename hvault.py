from ansible.module_utils.basic import *
import requests

def main():
	global module
        module = AnsibleModule(
                argument_spec  = dict(
                        host  = dict(required=True, type='str'),
                        rootkey = dict(required=False, type='str'),
                        method = dict(required=False, default='GET', type='str'),
			status_code = dict(required=False, default=[200], type='list'),
			action = dict(required=False, default='status', type='str')
                        )
                )
        if module.params['action'] == "seal-status":
		url = "http://"+module.params['host']+":8200/v1/sys/seal-status"
                vault_status(url)

        if module.params['action'] == "status":
		url = "http://"+module.params['host']+":8200/v1/sys/init"
                vault_status(url)

def vault_status(url):
	stdout = requests.get(url)
	if stdout.status_code not in module.params['status_code']:
		msg = 'Status code was not %s' % module.params['status_code']
		module.fail_json(msg=msg)
        else:
		module.exit_json(changed=True, responce=stdout.json())
	
if __name__ == '__main__':
        main()
