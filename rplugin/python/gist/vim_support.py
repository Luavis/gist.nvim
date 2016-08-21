from os import path

__author__ = "Luavis"
__name__ = "vim_support"



class VimSupport(object):
    """Python neovim support method(Some code are copy from YCM plugin)."""

    def __init__(self, nvim):
        """Vim support class constructor."""
        self.nvim = nvim

    def create_preview(self, name):
        """Create preview window."""
        self.nvim.command('silent! pedit! ' + name)

    def close_preview(self):
        """Close the preview window if it is present, otherwise do nothing."""
        self.nvim.command('silent! pclose!')

    def write_to_preview(self, msg):
        """Write to new preview window named `tempname` with msg."""
        self.close_preview()
        self.create_preview(self.nvim.eval('tempname()'))

        if self.jump_to_preview():
            self.nvim.current.buffer.options['modifiable'] = True
            self.nvim.current.buffer.options['readonly'] = False

            self.nvim.current.buffer[:] = msg.splitlines()

            self.nvim.current.buffer.options['buftype'] = 'nofile'
            self.nvim.current.buffer.options['swapfile'] = False
            self.nvim.current.buffer.options['modifiable'] = False
            self.nvim.current.buffer.options['readonly'] = True

            # We need to prevent closing the window causing a warning about unsaved
            # file, so we pretend to Vim that the buffer has not been changed.
            self.nvim.current.buffer.options['modified'] = False

            self.jump_to_previous()
        else:
            self.echo_text(msg)

    def echo_text(self, text, log_as_message=True):
        for line in text.split('\n'):
            command = 'echom' if log_as_message else 'echo'
            self.nvim.command("{0} '{1}'".format(command, self.escape_for_vim(text)))

    def escape_for_vim(self, text):
        return text.replace("'", "''")

    def jump_to_preview(self):
        """Jump the vim cursor to the preview window, which must be active. Returns
        boolean indicating if the cursor ended up in the preview window."""
        self.nvim.command('silent! wincmd P')
        return self.nvim.current.window.options['previewwindow']

    def jump_to_previous(self):
        """Jump the vim cursor to its previous window position."""
        self.nvim.command('silent! wincmd p')

    def create_or_get_buffer(self, name):
        """Create new buffer with name if it is present, otherwise create new one."""
        for b in self.nvim.buffers:
            bname = path.basename(b.name)
            if bname == name:
                return b

        # Create new buffer
        self.nvim.command('set splitbelow')
        self.nvim.command('new')
        self.nvim.command('setlocal buftype=nofile noswapfile ro')
        self.nvim.command('res 2')

        b = self.nvim.current.buffer
        b.name = name

        return b

    def _clear_buffer(self, buffer):
        buffer[:] = []
