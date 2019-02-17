from observer import st
import os.path
import sys
import json
import re

class Formatter:
    def __init__(self):
        self._options = st.ST.options()['formatter']
        self._keywords = {
            'include': re.compile('{\include\s+(?P<include_name>\w+)\W*}')
        }

    def format(self, message):
        st.ST.debugger().print("Incoming formatter", message)
        return self.process_message(self.get_template_content(message, message['rule_name']), message)

    def replace_variable(self, template, needle, replacement):
        variable = '{$%s}' % needle
        if variable in template:
            return template.replace(variable, replacement)
        return template

    def replace_variables(self, template, message):
        for dt_part in 'YmdHMS':
            template = self.replace_variable(
                template, dt_part, message['timestamp'].strftime('%{0}'.format(dt_part)))
        for key in message:
            if key == 'timestamp':
                template = self.replace_variable(
                    template, key, message['timestamp'].strftime('%Y.%m.%d %H:%M:%S'))
            else:
                template = self.replace_variable(template, key, message[key])
        message.pop('timestamp', None)
        template = self.replace_variable(
            template, '__all__', json.dumps(message, sort_keys=True, indent=4))
        return template

    def replace_includes(self, template, message):
        match_result = self._keywords['include'].search(template)
        # st.ST.debugger().print("Template matched data", [template, match_result])
        if match_result:
            data = match_result.groupdict()
            st.ST.debugger().print("Template include data", data)
            return self.replace_includes(re.sub('{{\include\s+{0}\W*}}'.format(data['include_name']), self.get_template_content(message, data['include_name']), template), message)
        return template

    def process_message(self, template, message):
        return self.replace_variables(self.replace_includes(template, message), message)

    def get_template_content(self, message, template_name):
        try:
            return self.try_get_template_content(message['output_plugin_name'], template_name)
        except Exception:
            pass
        try:
            return self.try_get_template_content('', template_name)
        except Exception:
            pass
        try:
            return self.try_get_template_content(message['output_plugin_name'], 'default')
        except Exception:
            pass
        try:
            return self.try_get_template_content('', 'default')
        except Exception:
            pass
        print("Can not find any template! Tryed: ")
        print(self.construct_template_filename(message['output_plugin_name'], template_name))
        print(self.construct_template_filename('', template_name))
        print(self.construct_template_filename(message['output_plugin_name'], 'default'))
        print(self.construct_template_filename('', 'default'))
        sys.exit()

    def try_get_template_content(self, folder, file):
        filename = self.construct_template_filename(folder, file)
        if os.path.isfile(filename):
            return self.load_template_content(filename)
        print('Template not exists: ', filename)
        raise Exception('File not found')

    def construct_template_filename(self, output_plugin_name, rule_name):
        return '{0}/{1}/{2}.tpl'.format(self._options['templates_path'], output_plugin_name, rule_name)

    def load_template_content(self, filename):
        with open(filename, 'r') as stream:
            return stream.read().strip()
