from sphinx.domains.changeset import versionlabels, VersionChange
from sphinx.locale import _  # just to suppress warnings

try:
    from sphinx.domains.changeset import versionlabel_classes
except ImportError:
    # versionlabel_classes doesn't exist in old Sphinx versions.
    UPDATE_VERIONLABEL_CLASSES = False
else:
    UPDATE_VERIONLABEL_CLASSES = True


labels = ("versionadded", "versionaddedold", "versionchanged", "versionchangedold", "deprecated", "deprecatedold", "versionextended", "versionextendedold")


def set_version_formats(app, config):
    for label in labels:
        versionlabels[label] = _(getattr(config, f"{label}_format"))


def setup(app):
    app.add_directive("versionextended", VersionChange)
    app.add_directive("versionaddedold", VersionChange)
    app.add_directive("versionchangedold", VersionChange)
    app.add_directive("deprecatedold", VersionChange)
    app.add_directive("versionextendedold", VersionChange)

    versionlabels["versionextended"] = "Extended in pygame-ce %s"
    versionlabels["versionaddedold"] = "New in pygame %s"
    versionlabels["versionchangedold"] = "Changed in pygame %s"
    versionlabels["deprecatedold"] = "Deprecated since pygame %s"
    versionlabels["versionextendedold"] = "Extended in pygame %s"


    if UPDATE_VERIONLABEL_CLASSES:
        versionlabel_classes["versionextended"] = "extended"
        versionlabel_classes["versionaddedold"] = "added"
        versionlabel_classes["versionchangedold"] = "changed"
        versionlabel_classes["deprecatedold"] = "deprecated"
        versionlabel_classes["versionextendedold"] = "extended"

    for label in labels:
        app.add_config_value(
            f"{label}_format", str(versionlabels[label]), "env"
        )

    app.connect("config-inited", set_version_formats)
