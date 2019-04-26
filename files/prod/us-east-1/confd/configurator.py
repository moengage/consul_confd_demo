#!/usr/bin/env python
import json
import os
import yaml


class ConfigurationGenerator(object):
    """ Configurator
    """
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

    def __init__(self):
        """ Initialize anything you will be using later on """
        self.templates = []

    @classmethod
    def create_generic_template(cls):
        if not os.path.exists(cls.GENERIC_TEMPLATE_FILEPATH):
            with open(cls.GENERIC_TEMPLATE_FILEPATH, 'w') as fp:
                fp.write(cls.GENERIC_TEMPLATE)


    def _get_templates(self):
        return self.templates

    def _set_templates(self, templates):
        assert type(templates) == list
        self.templates = templates

    def identify_service(self):
        """
        Implement logic to identify services
        """
        # These are machine identifier, you can implement your own logic here to
        # identify services. For us, every physical instance contains a file with
        # details such as which business unit and service the instance belongs to, aws
        # account id, region, environment (staging/prod/qa), consul acl token etc.
        self.business = "business_unit"
        self.service  = "service0"

    def parse_top(self):
        """
        Implement logic to parse top.yml and generate a list of templates which
        needs to be fetched from consul to manage current service
        """
        # As I mentioned If you wish to change top.yml format feel
        # free to implement your own and change following accordingly
        # For us, we follow this:
        # commons:
        # - all common templates
        #
        # Business:
        # - service_name:
        #   - all template for these instances
        # - service_name:
        #   - all template for these instances
        with open(self.TOP_FILEPATH, 'r') as fp:
            content = yaml.load(fp)
            templates = content.get('commons', [])
            all_fabtag_per_business = content.get(self.business, [])
            for tag in all_tag_per_business:
                templates.extend(tag.get(self.service, []))
            self._set_templates(templates)

    def generate_templates(self):
        for line in self._get_templates():
            key = line.strip()
            # This is not what we use at moengage
            # Confd doesn't manage files which were created before, but
            # later the templates got removed, the files should also get removed.
            # To keep track of this, we added a layer to keep track of
            # confd generated files. But for this demo, let's simplify
            # storage by following line
            filename = key.replace('/', '-').replace('.', '-')
            FILEPATH = self.INTERMEDIATE_FILEPATH.format(filename=filename)
            prefix, key = key.rsplit('/', 1)
            if not os.path.exists(self.FILEPATH):
                with open(self.FILEPATH, 'w') as fp:
                    fp.write(
                        self.CONFIG_TEMPLATE.format(
                            src=self.GENERIC_TEMPLATE_FILENAME,
                            filename=filename,
                            prefix=prefix,
                            key=key,
                            reload_cmd=self.RELOAD_CMD
                        )
                    )

if __name__ == '__main__':
    cg = ConfigurationGenerator()
    cg.create_generic_template()
    cg.identify_service()
    cg.parse_top()
    cg.generate_templates()
