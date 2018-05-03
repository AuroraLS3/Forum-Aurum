from misaka import SaferHtmlRenderer


class CustomMisakaRenderer(SaferHtmlRenderer):
    def blockquote(self, content):
        return '<blockquote class="blockquote">{}</blockquote>'.format(content)