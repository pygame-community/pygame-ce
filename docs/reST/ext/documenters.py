import autoapi
import autoapi.documenters
from autoapi._objects import PythonClass
import re


def build_signatures(object):
    name = object.short_name

    if isinstance(object, PythonClass):
        if object.constructor is not None:
            object = object.constructor
            object.obj["return_annotation"] = name
            object.obj["overloads"] = [
                (arg, name) for arg, _ in object.obj["overloads"]
            ]

        else:
            for child in object.children:
                if child.short_name == "__new__":
                    object = child
                    break

    if object is None or object.obj.get("args", None) is None:
        return

    sigs = [(object.obj["args"], object.obj["return_annotation"])]
    sigs.extend(object.obj["overloads"])

    for args, ret in sigs:
        arg_string = ""
        for modifier, arg_name, _, default in args:
            modifier = modifier or ""
            arg_name = arg_name or ""
            default = default or ""

            if default:
                default = "=" + default
            arg_string += f", {modifier}{arg_name}{default}"

        if arg_string:
            arg_string = arg_string[2:]

        if object.obj["type"] == "property":
            arg_string = ""
        else:
            arg_string = f"({arg_string})"

        if ret.count("[") > 2 or ret.count(",") > 3:
            ret = ret.split("[")[0]
            if ret in ("Optional", "Union"):
                ret = "..."

        # Shorten "pygame.module.X" types to "X"
        ret = re.sub(r"pygame(.[a-zA-Z0-9_]+)+", lambda x: x.group(1)[1:], ret)
        ret = ret.replace("Ellipsis", "...")

        yield f"| :sg:`{name}{arg_string} -> {ret}`"


def get_doc(env, obj):
    if obj.docstring:
        return obj.docstring

    # If we don't already have docs, check if a python implementation exists of this
    # module and return its docstring if it does
    python_object = env.autoapi_all_objects.get(
        obj.id.replace("pygame", "src_py"), None
    )
    if python_object is not None:
        return python_object.docstring

    return ""


class AutopgDocumenter(autoapi.documenters.AutoapiDocumenter):
    def format_signature(self, **kwargs):
        return ""

    def get_doc(self, encoding=None, ignore=1):
        return [get_doc(self.env, self.object).splitlines()]

    def add_directive_header(self, sig: str) -> None:
        super().add_directive_header(sig)
        if "module" in self.objtype:
            sourcename = self.get_sourcename()
            self.add_line(f"   :synopsis: {self.get_doc()[0][0]}", sourcename)

    def get_object_members(self, want_all):
        members_check_module, members = super().get_object_members(want_all)
        members = (
            member
            for member in members
            if not member.object.imported and get_doc(self.env, member.object) != ""
        )

        return members_check_module, members

    def process_doc(self, docstrings):
        for docstring in docstrings:
            if not docstring:
                continue

            yield f"| :sl:`{docstring[0]}`"

            if "args" in self.object.obj or hasattr(self.object, "constructor"):
                yield from build_signatures(self.object)
            else:
                annotation = self.object.obj.get("annotation", None)
                if annotation is not None:
                    if annotation.count("[") > 2 or annotation.count(",") > 3:
                        annotation = "..."
                    yield f"| :sg:`{self.object.short_name} -> {annotation}`"

            yield from docstring[1:]

        yield ""


def setup(app):
    names = [
        "function",
        "property",
        "decorator",
        "class",
        "method",
        "data",
        "attribute",
        "module",
        "exception",
    ]

    for name in names:
        capitalized = name.capitalize()
        app.add_autodocumenter(
            type(
                f"Autopg{capitalized}Documenter",
                (
                    AutopgDocumenter,
                    getattr(autoapi.documenters, f"Autoapi{capitalized}Documenter"),
                ),
                {"objtype": f"pg{name}"},
            )
        )
