from pygments import highlight, lexers
from pygments.style import Style
from pygments.formatters import HtmlFormatter
from pygments.lexer import RegexLexer, include, bygroups, words, combined
from pygments.token import (
    Keyword,
    Name,
    Comment,
    String,
    Error,
    Number,
    Operator,
    Whitespace,
    Punctuation,
)

__all__ = ["GDScriptBetterLexer", "GDScriptStyle"]

class GDScriptBetterLexer(RegexLexer):
    """
    For GDScript source code.
    """

    name = "GDScriptBetter"
    url = 'https://www.godotengine.org'
    aliases = ["gdscriptbetter", "gd"]
    filenames = ["*.gd"]
    mimetypes = ["text/x-gdscript", "application/x-gdscript"]

    # taken from pygments/gdscript.py
    def innerstring_rules(ttype):
        return [
            # the old style '%s' % (...) string formatting
            (r"%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?"
                "[hlL]?[E-GXc-giorsux%]",
                String.Interpol),
            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"%\n]+', ttype),
            (r'[\'"\\]', ttype),
            # unhandled string formatting sign
            (r"%", ttype),
            # newlines are an error (use "nl" state)
        ]

    tokens = {
        "whitespace": [(r'\s+', Whitespace)],
        "comment": [
            (r"#.*$", Comment.Single),
            # """ """ and ''' '''
            (r'^(\s*)([rRuUbB]{,2})("""(?:.|\n)*?""")',
                bygroups(Whitespace, String.Affix, String.Doc)),
            (r"^(\s*)([rRuUbB]{,2})('''(?:.|\n)*?''')",
                bygroups(Whitespace, String.Affix, String.Doc)),
        ],
        "punctuation": [
            (r"[]{}(),;[]", Punctuation),
            (r":\n", Punctuation),
            (r"\\", Punctuation),
        ],
        "keywords": [
            (words(("and", "in", "not", "or", "as", "breakpoint", "class",
                    "class_name", "extends", "is", "setget", "signal",
                    "tool", "const", "enum", "export", "onready", "static",
                    "var", "break", "continue", "if", "elif", "else", "for",
                    "pass", "return", "match", "while", "remote", "master",
                    "puppet", "remotesync", "mastersync", "puppetsync"),
                    suffix=r"\b"), Keyword),
        ],
        "builtins": [
            (words(("yield", "true", "false", "PI", "TAU", "NAN", "INF"),
                    prefix=r"(?<!\.)", suffix=r"\b"),
                Name.Builtin),
            (words(("Color8", "ColorN", "abs", "acos", "asin", "assert", "atan",
                    "atan2", "bytes2var", "ceil", "char", "clamp", "convert",
                    "cos", "cosh", "db2linear", "decimals", "dectime", "deg2rad",
                    "dict2inst", "ease", "exp", "floor", "fmod", "fposmod",
                    "funcref", "hash", "inst2dict", "instance_from_id", "is_inf",
                    "is_nan", "lerp", "linear2db", "load", "log", "max", "min",
                    "nearest_po2", "pow", "preload", "print", "print_stack",
                    "printerr", "printraw", "prints", "printt", "rad2deg",
                    "rand_range", "rand_seed", "randf", "randi", "randomize",
                    "range", "round", "seed", "sign", "sin", "sinh", "sqrt",
                    "stepify", "str", "str2var", "tan", "tan", "tanh",
                    "type_exist", "typeof", "var2bytes", "var2str", "weakref"
                    ), prefix=r"(?<!\.)", suffix=r"\b"),
                Name.Builtin.Function),
            (r"((?<!\.)(self)" r")\b", Name.Builtin.Pseudo),
            (words(("bool", "int", "float", "String", "NodePath", "Vector2",
                    "Rect2", "Transform2D", "Vector3", "Rect3", "Plane", "Quat",
                    "Basis", "Transform", "Color", "RID", "Object", "NodePath",
                    "Dictionary", "Array", "PackedByteArray", "PackedInt32Array",
                    "PackedInt64Array", "PackedFloat32Array", "PackedFloat64Array",
                    "PackedStringArray", "PackedVector2Array", "PackedVector3Array",
                    "PackedColorArray", "null", "void"),
                    prefix=r"(?<!\.)", suffix=r"\b"),
                Name.Builtin.Type),
        ],
        "operator": [
            (r"!=|==|<<|>>|&&|\+=|-=|\*=|/=|%=|&=|\|=|\|\||:=|[-~+/*%=<>&^.!|$]", Operator),
            (r"(in|and|or|not)\b", Operator.Word),
        ],
        "numbers": [
            (r"(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?j?", Number.Float),
            (r"\d+[eE][+-]?[0-9]+j?", Number.Float),
            (r"0[xX][a-fA-F0-9]+", Number.Hex),
            (r"\d+j?", Number.Integer),
        ],
        "name": [(r"[a-zA-Z_]\w*", Name)],
        "funcname": [(r"[a-zA-Z_]\w*", Name.Function, "#pop")],
        "typehint": [
            (r"[a-zA-Z_]\w*", Name.Class, "#pop"),
        ],
        "stringescape": [
            (
                r'\\([\\abfnrtv"\']|\n|N\{.*?\}|u[a-fA-F0-9]{4}|'
                r"U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})",
                String.Escape,
            )
        ],
        "strings-single": innerstring_rules(String.Single),
        "strings-double": innerstring_rules(String.Double),
        "double_quotes": [
            (r'"', String.Double, "#pop"),
            (r'\\\\|\\"|\\\n', String.Escape),  # included here for raw strings
            include("strings-double"),
        ],
        "single_quotes": [
            (r"'", String.Single, "#pop"),
            (r"\\\\|\\'|\\\n", String.Escape),  # included here for raw strings
            include("strings-single"),
        ],
        "triple_double_quotes": [
            (r'"""', String.Double, "#pop"),
            include("strings-double"),
            include("whitespace"),
        ],
        "triple_single_quotes": [
            (r"'''", String.Single, "#pop"),
            include("strings-single"),
            include("whitespace"),
        ],
        "root": [
            include("whitespace"),
            include("comment"),
            include("punctuation"),

            # strings
            ('([rR]|[uUbB][rR]|[rR][uUbB])(""")',
                bygroups(String.Affix, String.Double),
                "triple_double_quotes"),
            ("([rR]|[uUbB][rR]|[rR][uUbB])(''')",
                bygroups(String.Affix, String.Single),
                "triple_single_quotes"),
            ('([rR]|[uUbB][rR]|[rR][uUbB])(")',
                bygroups(String.Affix, String.Double),
                "double_quotes"),
            ("([rR]|[uUbB][rR]|[rR][uUbB])(')",
                bygroups(String.Affix, String.Single),
                "single_quotes"),
            ('([uUbB]?)(""")',
                bygroups(String.Affix, String.Double),
                combined("stringescape", "triple_double_quotes")),
            ("([uUbB]?)(''')",
                bygroups(String.Affix, String.Single),
                combined("stringescape", "triple_single_quotes")),
            ('([uUbB]?)(")',
                bygroups(String.Affix, String.Double),
                combined("stringescape", "double_quotes")),
            ("([uUbB]?)(')",
                bygroups(String.Affix, String.Single),
                combined("stringescape", "single_quotes")),

            include("operator"),
            include("keywords"),
            (r"(func)(\s+)", bygroups(Keyword, Whitespace), "funcname"),
            # TODO: make the discernment if the type is Name.Builtin
            (r"\b(\w+)\s*(:)( )", bygroups(Name.Variable, Punctuation, Whitespace), "typehint"),
            (r":", Punctuation), # HACK: fix missed colon captures

            include("builtins"),
            include("name"),
            include("numbers"),
        ],
    }

class GDScriptStyle(Style):
    background_color = "#1d2229"

    styles = {
        Whitespace:               "#bbbbbb", # for whitespace
        Comment:                  "#cdcfd2", # any kind of comments
        Punctuation:              "#abc9ff", # punctuation (e.g. [!.,])

        Keyword:                  "#ff7085", # Any kind of keyword; especially if it doesn’t match any of the subtypes

        Operator:                 "#abc9ff", # For any punctuation operator (e.g. +, -)
        Operator.Word:            "#ff7085", # For any operator that is a word (e.g. not, in)

        Name.Builtin:             "#42ffc2", # names that are available in the global namespace (NOT USED)
        Name.Builtin.Type:        "#42ffc2", # types that are available in the global namespace
        Name.Builtin.Function:    "#a3a3f5", # functions that are available in the global namespace
        Name.Function:            "#57b3ff", # function names
        Name.Class:               "bold #FF0000", # class names / declarations
        Name.Variable:            "#bce0ff", # variable names
        Name.Constant:            "#bce0ff", # constant names
        Name.Decorator:           "#ffb373", # decorators / annotations (TODO)

        String:                   "#ffeda1", # string literals
        String.Doc:               "#ffeda1", # doc string literal
        String.Interpol:          "#ffeda1", # interpolated parts (e.g. %s)
        String.Escape:            "#ffeda1", # escape sequences

        Number:                   "#a1ffe0", # number literal

        Error:                    "border:#FF0000" # represents lexer errors (very useful for debugging)
    }
