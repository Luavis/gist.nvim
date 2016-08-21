import neovim
try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen
import json
from os import path
from vim_support import VimSupport

API_DOMAIN = "https://api.github.com"


@neovim.plugin
class GistPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('GistSave', range='', nargs='*')
    def gist_save(self, args, range):
        target_buffer = self.nvim.current.buffer

        filename = path.basename(target_buffer.name)
        content = '\n'.join(target_buffer[:])
        vim_support = VimSupport(self.nvim)
        vim_support.write_to_preview('Gist saving...')

        url = self._post_gist(filename, content)
        vim_support.write_to_preview(url)

    def _post_gist(self, filename, content):
        api_data = {
            'public': True,
            'files': {
                filename: {
                    'content': content,
                },
            },
        }

        req = Request(
            API_DOMAIN + '/gists',
            data=json.dumps(api_data).encode('utf-8')
        )

        res = urlopen(req)
        response = json.loads(res.read().decode('utf-8'))
        return response['html_url']

