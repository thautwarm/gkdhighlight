from .impl import to_latex, import_style
from typing import cast
import gkdtex.developer_utilities as dev

def import_(style: dev.Group, *, self: dev.Interpreter, tex_print):
    style = dev.eval_to_string(self, style.obj)
    import_style(style, tex_print)

def highlight(language: dev.Group, code: dev.Group, *, self: dev.Interpreter, tex_print, style : 'str | dev.Group'= '', expand=None):
    if expand:
        expand = cast(dev.Group, expand)
        expand = eval(dev.get_raw_from_span_params(self.src, expand.offs).strip())

    if not isinstance(style, str):
        style = cast(dev.Group, style)
        if expand:
            style = dev.eval_to_string(self, style.obj)
        else:
            style = dev.get_raw_from_span_params(self.src, style.offs)
    style = style.strip()

    if expand:
        language = dev.eval_to_string(self, language.obj)
    else:
        language = dev.get_raw_from_span_params(self.src, language.offs)
    language = language.strip()

    if expand:
        code = dev.eval_to_string(self, code.obj)
    else:
        code = dev.get_raw_from_span_params(self.src, code.offs)
    to_latex(code, language, style, tex_print)


class GkdInterface:
    @staticmethod
    def load(self, tex_print):

        tex_print(
        r"""
\usepackage{amsmath}
\usepackage{xcolor}        
        """)
        import_style("pastie", tex_print)
        self.globals['gkd@highlight'] = highlight
        self.globals['gkd@loadpygments'] = import_

