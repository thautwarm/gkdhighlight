import io
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.lexer import Lexer
from pygments.style import Style
from functools import lru_cache

_xs = 'abcdefghijklmnopqrstuvwxyz'
_N = len(_xs)
def _i2c(i: int):
    while i:
        yield _xs[i % _N]
        i = i // _N


class AutoName(dict):
    def __missing__(self, k):
        self[k] = v = 'GKDHLPYGMENT{}'.format(''.join(_i2c(len(self))))
        return v

LOAD_STYLES = AutoName()
last_style = ["pastie"]

def mk_style(style: dict):
    cmd = r'\texttt{#1}'
    color = style.get('color', None)
    if color:
         cmd = '\\textcolor[rgb]{{{}, {}, {}}}{{{}}}'.format(
            int(color[0:2], 16) / 255.0,
            int(color[2:4], 16) / 255.0,
            int(color[4:6], 16) / 255.0,
            cmd
        )

    if style.get('bold', None):
        cmd = '\\textbf{{{}}}'.format(
            cmd
        )

    if style.get('italic', None):
        cmd = '\\textit{{{}}}'.format(cmd)

    if  style.get('underline', None):
        cmd = '\\underline{{{}}}'.format(cmd)

    if style.get('roman', None):
        cmd = "\\textrm{{{}}}".format(cmd)
    return cmd

def import_style(style: str, tex_print):
    last_style[0] = style
    _import_style(style, tex_print)

@lru_cache(maxsize=None)
def _import_style(style: str, tex_print):
    style = get_style_by_name(style)
    for tk, style_dict in iter(style):
        k = (style, tk)
        if not LOAD_STYLES.get(k):
            n = LOAD_STYLES[k]
            impl = mk_style(style_dict)
            tex_print(f"\\newcommand{{\\{n}}}[1]{{{impl}}}\n")

def get_style(*k):
    n = LOAD_STYLES.get(k)
    if not n:
        raise KeyError(k)
    return n

escape_table = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\texttt{\~{}}',
    '^': r'\^{}',
    '\\': r'$\backslash$',
    '\n': r'\hfill\\',
    ' ': r'\phantom{t}',
    '[': r'\normalsize[',
    ']': r'\normalsize]'
}
@lru_cache()
def escape_cache(x: str):
    chars = []
    for ch in x:
        chars.append(escape_table.get(ch, ch))
    return ''.join(chars)

def escape(x: str):
    if len(x) < 9:
        return escape_cache(x)
    buf = io.StringIO()
    for ch in x:
        buf.write(escape_table.get(ch, ch))
    return buf.getvalue()


def to_latex(text: str, lang: str, style: str, tex_print):
    style = style or last_style[0] # type: str
    lexer = get_lexer_by_name(lang) # type: Lexer
    generator = lexer.get_tokens(text)
    style =  get_style_by_name(style) # type: Style
    tex_print(r'\noindent ')
    for scope, text in generator:
        n = get_style(style, scope)
        text = escape(text)
        rendered = f'\\{n}{{{text}}}'
        tex_print(rendered)
