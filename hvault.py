from ansible.module_utils.basic import *
import requests
import urllib2

def main():
	global module
        module = AnsibleModule(
                argument_spec  = dict(
                        host  = dict(required=True, type='str'),
			port  = dict (required=False, default=8200, type='int'),
                        method = dict(required=False, default='GET', type='str'),
			status_code = dict(required=False, default=[200], type='list'),
			root_token = dict(required=False, type='str'),
			action = dict(required=False, default='status', type='str')
                        )
                )
        if module.params['action'] == "seal-status":
		url = "http://%s:%s/v1/sys/seal-status" % (module.params['host'], module.params['port'])
                vault_status(url)

        if module.params['action'] == "status":
		url = "http://%s:%s/v1/sys/init" % (module.params['host'], module.params['port'])
                vault_status(url)
	if module.params['action'] == "seal":
		url = "http://%s:%s/v1/sys/seal" % (module.params['host'], module.params['port'])
		#headers = {'X-Vault-Token': module.params['root_token'] }
		vaultSeal(url)

def vault_status(url):
	stdout = requests.get(url)
	if stdout.status_code not in module.params['status_code']:
		msg = 'Status code was not %s :: Responded Status code %s' % (module.params['status_code'], stdout.status_code)
		module.fail_json(msg=msg)
        else:
		module.exit_json(changed=False, responce=stdout.json())

def vaultSeal(url):
	stdout = requests.put(url, headers={"X-Vault-Token": module.params['root_token']})

        if stdout.status_code == 204:
                module.exit_json(changed=False, responce="Success")
        else:
                msg = 'Status code was not %s :: Responded Status code %s' % (module.params['status_code'],  stdout.status_code)
                module.fail_json(msg=msg)

	
	
if __name__ == '__main__':
        main()
