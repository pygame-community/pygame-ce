import autoapi
import autoapi.documenters
from autoapi._objects import PythonClass


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

        if ret.count("[") > 2 or ret.count(",") > 3:
            ret = "..."

        yield f"| :sg:`{name}({arg_string}) -> {ret}`"


class AutopgDocumenter(autoapi.documenters.AutoapiDocumenter):
    def format_signature(self, **kwargs):
        return ""

    def get_doc(self, encoding=None, ignore=1):
        if self.object.docstring:
            return super().get_doc(encoding, ignore)

        # If we don't already have docs, check if a python implementation exists of this
        # module and return its docstring if it does
        python_object = self.env.autoapi_all_objects.get(
            self.object.id.replace("pygame", "src_py"), None
        )
        if python_object is not None:
            return [python_object.docstring.splitlines()]

        return [""]

    def process_doc(self, docstrings: list[str]):
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
