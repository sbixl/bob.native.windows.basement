from bob.errors import ParseError
import os, os.path
import platform
import subprocess
import glob

cache = {}

def vsvars2019(args, **options):
    if len(args) < 2:
        raise ParseError("$(vsvars2019,VAR,ARCH,...) expects at least two arguments")

    system = platform.uname().system
    if system.startswith("MSYS_NT"):
        isMSYS = True
    elif system == "Windows":
        isMSYS = False
    else:
        raise ParseError("Unsupported system for $(vsvars2019,...): " + system)

    try:
        varname = args[0]
        vsvars_args = args[1:]
        vswargs = (os.path.join(os.environ["ProgramFiles(x86)"],
                                "Microsoft Visual Studio/Installer/vswhere.exe"),
                '-property', 'installationPath',
                '-version', '[16.0,17.0)',
                '-products', 'Microsoft.VisualStudio.Product.BuildTools',
                '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64')

        tag = tuple(vsvars_args)
        if tag not in cache:
            r = subprocess.check_output(vswargs, universal_newlines=True).strip()
            vsvarsall = os.path.join(r, "VC/Auxiliary/Build/vcvarsall.bat")
            r = subprocess.check_output([vsvarsall] + vsvars_args + ['&&', 'set'],
                universal_newlines=True)
            env = {}
            for l in r.splitlines():
                k,sep,v = l.strip().partition("=")
                k = k.upper()
                if k == 'PATH' and isMSYS:
                    # convert to POSIX path to be mergeable
                    v = subprocess.check_output(["cygpath", "-u", "-p", v], universal_newlines=True).strip()
                elif k == 'PATH':
                    # Only append the VS specific parts of the PATH variable and not the paths
                    # again which are already part of the SYSTEM/USER Path variable. If we will
                    # not this, the paths appended by bob during build time will be overwritten
                    # (first come first served) and some tool is picked up from the local file
                    # system instead of the one provided by the recipes of bob (e.g. a different
                    # python executable may be chosen in the build-step of a recipe)
                    #
                    #  Order in which the paths are stored in the PATH variable:
                    #
                    #      - VSENV_PATHS (the paths we gather in this script)
                    #      - BOB_BATHS   (the paths bob will append during execution)
                    #      - USER_PATHS  (if not provided by bob, use as last chance tools from the host)
                    #
                    system_paths = os.getenv('PATH').split(";")
                    vsenv_paths = v.split(";")
                    # rebuild the VSENV path variable
                    v = ""
                    for path in vsenv_paths:
                        # do not append duplicates already stored in the PATH variable
                        if path not in system_paths:
                            if v != "":
                                v += ";"
                            v += path
                env[k] = v
            cache[tag] = env

        return cache[tag][varname]
    except (OSError, subprocess.SubprocessError) as e:
        raise ParseError("$(vsvars2019) failed: " + str(e))

manifest = {
    'apiVersion' : "0.15",
    'stringFunctions' : {
        "vsvars2019" : vsvars2019
    },
}
