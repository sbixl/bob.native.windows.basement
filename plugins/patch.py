import os
import platform
import subprocess

from bob.errors import ParseError


def patch(args, **options):
    system = platform.uname().system
    if system != "Windows":
        raise ParseError("Unsupported system for $(patch,...): " + system)

    try:
        result = subprocess.check_output("{} {}".format("where", "git"), stderr=subprocess.STDOUT)
        git_paths = result.decode().split('\r\n')

        if None is not git_paths:
            for git_path in git_paths:
                git_root_path = os.path.dirname(os.path.dirname(git_path))
                patch_path = os.path.join(git_root_path, "usr", "bin")
                if os.path.exists(patch_path):
                    # check if patch.exe exists
                    if os.path.exists(os.path.join(patch_path, "patch.exe")):
                        return patch_path
            raise ParseError("$(patch) failed: Could not find 'patch.exe' in Git root!")
        else:
            raise ParseError("$(patch) failed: Git for Windows is not installed ony your HOST!")
    except subprocess.CalledProcessError as e:
        raise ParseError("$(patch) failed: " + str(e))


manifest = {
    "apiVersion": "0.15",
    "stringFunctions": {"patch": patch},
}
