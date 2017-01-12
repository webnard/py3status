# -*- coding: utf-8 -*-
"""
Display the amount of windows in your i3 scratchpad.

Configuration parameters:
    cache_timeout: How often we refresh this module in seconds (default 5)
    format: string to print (default '{counter} ⌫')

Format placeholders:
    {counter} number of scratchpad windows

@author shadowprince
@license Eclipse Public License
"""

import i3


def find_scratch(tree):
    if tree["name"] == "__i3_scratch":
        return tree
    else:
        for x in tree["nodes"]:
            result = find_scratch(x)
            if result:
                return result
        return None


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 5
    format = u"{counter} ⌫"

    class Meta:
        deprecated = {
            'format_fix_unnamed_param': [
                {
                    'param': 'format',
                    'placeholder': 'counter',
                    'msg': '{} should not be used in format use `{counter}`',
                },
            ],
        }

    def __init__(self):
        self.count = -1

    def scratchpad_counter(self):
        count = len(find_scratch(i3.get_tree()).get("floating_nodes", []))

        if self.count != count:
            transformed = True
            self.count = count
        else:
            transformed = False

        response = {
            'cached_until': self.py3.time_in(self.cache_timeout),
            'full_text': self.py3.safe_format(self.format, {'counter': count}),
            'transformed': transformed
        }

        #if count > 0:
        #    response['full_text'] = self.py3.safe_format(self.format, {'counter': count})

        # backward compatible (1/11/17)
        if self.hide_when_none and count == 0:
            response['full_text'] = ''

        return response


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
