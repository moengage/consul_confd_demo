[template]
src = "generic.tmpl"
dest = "/etc/service1/include.d/settings.py"
mode = "0644"
keys = [
  "settings.py",
]
prefix = "/consul_confd_demo/templates/prod/us-east-1/service1"
check_cmd = "sudo service1 -t"
reload_cmd = "sudo service service1 reload"
