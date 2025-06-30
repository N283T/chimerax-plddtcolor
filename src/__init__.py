# vim: set expandtab shiftwidth=4 softtabstop=4:

from chimerax.core.toolshed import BundleAPI


class _MyAPI(BundleAPI):
    api_version = 1

    @staticmethod
    def register_command(bi, ci, logger):
        from . import cmd
        if ci.name == "plddt":
            func = cmd.color_plddt
            desc = cmd.color_plddt_desc
        else:
            raise ValueError("Unknown command: %s" % ci.name)
        if desc.synopsis is None:
            desc.synopsis = ci.synopsis
        from chimerax.core.commands import register
        register(ci.name, desc, func)


bundle_api = _MyAPI()
