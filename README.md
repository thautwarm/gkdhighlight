## gkdhighlight

We hereby present `gkdhighlight`, a syntax highlighting library for GkdTeX.

No LaTeX dependencies other than `xcolor` and `asmmath`, no shell-escape, no compatibility issue introduced.

`pip install gkdhighlight` within 0.5 seconds.

```tex

\gkd@usepackage{gkdhighlight}

\begin{document}
...

\gkd@highlight{ocaml}{
    module FM = Functor(M)
    let res = print_endline FM.message
    }
\gkd@loadpygments{colorful}
\gkd@highlight{python}{
    class S:
        def f(self, x):
            return print(1 + x)
}
\gkd@loadpygments{perldoc}
\gkd@highlight{haskell}{^style perldoc}{
    data NAT repr = NAT { Z :: repr, S :: repr -> repr }
    data Nat
        = Z
        | S Nat
}
```
![example0.PNG](example0.PNG)

