[template]
src = "generic.tmpl"
dest = "/etc/confd/workdir/configurator.py"
mode = "0644"
keys = [
  "configurator.py",
]
prefix = "/consul_confd_demo/files/prod/us-east-1/confd"
reload_cmd = "sudo python /etc/confd/workdir/configurator.py"
