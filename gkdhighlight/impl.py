import io
import re
import typing
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.lexer import Lexer, RegexLexer
from pygments.style import Style
from pygments.token import string_to_tokentype
from functools import lru_cache
NoEscape = string_to_tokentype("NoEscape")


@lru_cache(maxsize=None)
def allow_math_escape(base_lexer: typing.Type[RegexLexer], noescape):

    class ExtLexer(RegexLexer):
        name = base_lexer.name
        tokens = {
            **base_lexer.tokens,
            'root': [(noescape, NoEscape), *base_lexer.tokens['root']]
        }
    return ExtLexer()


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
    '_': r'{\textunderscore}',
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
def escape_cache(x: str, noescape):
    chars = []
    for ch in x:
        if ch in noescape:
            chars.append(ch)
        else:
            chars.append(escape_table.get(ch, ch))
    return ''.join(chars)

def escape(x: str, noescape):
    if len(x) < 9:
        return escape_cache(x, noescape)
    buf = io.StringIO()
    for ch in x:
        if ch in noescape:
            buf.write(ch)
        else:
            buf.write(escape_table.get(ch, ch))
    return buf.getvalue()


def to_latex(text: str, lang: str, style: str, tex_print, noescape: str):
    style = style or last_style[0] # type: str
    if noescape:
        lexer = allow_math_escape(type(get_lexer_by_name(lang)), noescape) # type: Lexer
    else:
        lexer = get_lexer_by_name(lang)
    generator = lexer.get_tokens(text)
    style =  get_style_by_name(style) # type: Style
    tex_print(r'\noindent ')
    for scope, text in generator:
        if scope is NoEscape:
            tex_print(text)
        else:
            n = get_style(style, scope)
            text = escape(text, noescape)
            rendered = f'\\{n}{{{text}}}'
            tex_print(rendered)
