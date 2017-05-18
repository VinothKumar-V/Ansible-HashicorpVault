from ansible.module_utils.basic import *
import requests

def main():
	global module
        module = AnsibleModule(
                argument_spec  = dict(
                        host  = dict(required=True, type='str'),
                        rootkey = dict(required=False, type='str'),
                        method = dict(required=False, default='GET', type='str'),
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
	
	module.exit_json(changed=True, responce=stdout)
	
if __name__ == '__main__':
        main()
