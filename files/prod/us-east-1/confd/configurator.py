#!/usr/bin/env python
import json
import os
import yaml


CONFD_CONFIG_DIR = "/etc/confd/conf.d/"
CONFD_TEMPLATE_DIR = "/etc/confd/templates/"
CONFIGURATOR_WORK_DIR = "/etc/confd/workdir/"
CONFIG_TEMPLATE = """[template]
src = '{src}'
dest = '/etc/confd/conf.d/orig{filename}.toml'
mode = '0644'
keys = ['{key}']
prefix = '{prefix}'
reload_cmd = "{reload_cmd}"
"""
GENERIC_TEMPLATE_FILENAME = 'generic.tmpl'
GENERIC_TEMPLATE_FILEPATH = CONFD_TEMPLATE_DIR + GENERIC_TEMPLATE_FILENAME
GENERIC_TEMPLATE = """{{range gets "/*"}}{{.Value}}{{end}}"""
TOP_FILENAME = "top.yml"
TOP_FILEPATH = CONFIGURATOR_WORK_DIR + TOP_FILENAME
INTERMEDIATE_FILENAME = 'intermediate{filename}.toml'
INTERMEDIATE_FILEPATH = CONFD_CONFIG_DIR + INTERMEDIATE_FILENAME
RELOAD_CMD = 'sudo python /etc/confd/workdir/configurator.py'


# These are machine identifier, you can implement your own logic here to
# identify services. For us, every physical instance contains a file with
# details such as which business unit and service the instance belongs to, aws
# account id, region, environment (staging/prod/qa), consul acl token etc.
business = "business_unit"
service  = "service0"


def main():
    if not os.path.isfile(TOP_FILEPATH):
        with open(TOP_FILEPATH, 'w') as fp:
            pass

    with open(TOP_FILEPATH, 'r') as fp:
        # Read top.yml
        content = yaml.load(fp)

        # Parser to parse top.yml and identify which configuration files needs
        # to be fetched from consul. If you wish to change top.yml formal feel
        # free to implement your own and change following accordingly
        templates = content.get('commons', [])
        all_fabtag_per_business = content.get(business, [])
        for tag in all_tag_per_business:
            templates.extend(tag.get(service, []))

        # Generate intermediate templates
        for line in templates:
            key = line.strip()
            # This is not what we use at moengage, for this POC this should work
            filename = key.replace('/', '-').replace('.', '-')
            if filename:
                FILEPATH = INTERMEDIATE_FILEPATH.format(filename=filename)
                prefix, key = key.rsplit('/', 1)
                if not os.path.exists(FILEPATH):
                    with open(FILEPATH, 'w') as fp:
                        fp.write(
                            CONFIG_TEMPLATE.format(
                                src=GENERIC_TEMPLATE_FILENAME,
                                filename=filename,
                                prefix=prefix,
                                key=key,
                                reload_cmd=RELOAD_CMD
                            )
                        )

    if not os.path.exists(GENERIC_TEMPLATE_FILEPATH):
        with open(GENERIC_TEMPLATE_FILEPATH, 'w') as fp:
            fp.write(GENERIC_TEMPLATE)

if __name__ == '__main__':
    main()
