# Previous note

Most of the recipes and classes included in this project were originally adopted from the
[basement project](https://github.com/BobBuildTool/basement). This repository adapts them for
native Windows and uses PowerShell as the scripting language instead of bash. The recipes and
classes were ported to PowerShell as far as practical to support native Windows builds without MSYS.

# Native Windows Basement

This basement project is a collection of useful recipes and classes that can be used by other
projects. Most importantly, it provides standard classes to handle common build systems and other
standard tasks. Optionally, an x86_64 Clang toolchain is available, and common GCC cross toolchains
are available by default.

# Prerequisites

* An x86_64 system with Windows 10 or Windows 11 (Windows 10 should also work)
* Windows system configuration
  * Make sure you can create symbolic links without administrative rights. Usually, you can enable
    this by switching to Developer Mode. If this does not work, enable it in your
    [security policy settings](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/create-symbolic-links).
  * [Enable long path support](https://www.msftnext.com/how-to-enable-ntfs-long-paths-in-windows-10/).

* Git for Windows (https://gitforwindows.org/)
* PowerShell 7 (`pwsh`) is required because the project does not use Windows PowerShell 5.x. The project was tested with version 7.6.6, and the executable must be available in the local `PATH` environment variable.
* Bob Build Tool (https://github.com/BobBuildTool/bob) with a minimum version of v1.3.0

# How to build

There is the possibility to choose between two different host toolchains.

By default, the MSVC 2026 compiler (v145) is configured as the host toolchain. If you want to use
Clang as the host toolchain, you can switch to it by modifying the environment variable
`ENABLE_X86_64_CLANG_HOST_TOOLCHAIN`, which is defined in the `default.yaml` file located in the root
directory of this repository.

```yaml
    # This will enable/disable the clang host toolchain if required by the user. If set to
    # "True" some initial tools will be bootstrapped using the native MSVC compiler because
    # they are required to build the clang toolchain. After building the clang toolchain, the
    # clang toolchain earns the role of the master host toolchain.
    # If set to "False" the MSVC compiler becomes the master host toolchain.
    ENABLE_X86_64_CLANG_HOST_TOOLCHAIN: "False"
```

While building the Clang host toolchain, take care to use a flat folder structure. Regardless of
whether or not long paths are enabled, if the paths are too long, the build process of the Clang
compiler will fail because some paths cannot be resolved, created, or deleted. The best way is to
clone the repository, for example under `C:\Work` or something similar.

Since there are currently no example projects that use this project as a layer, you can clone the
recipes and build them with Bob in development mode:

```shell
    git clone https://github.com/sbixl/bob.native.windows.basement.git
    cd bob.native.windows.basement
    # building all packages (native host toolchain is the default MSVC 2026 compiler)
    bob dev buildall
    # OR building all packages including a self-built Clang host toolchain
    bob dev buildall -DENABLE_X86_64_CLANG_HOST_TOOLCHAIN=True
```

---
**NOTE**

Building the Clang host toolchain is independent from the rest of the packages. Since it can take a
long time to build it, it should not affect other packages. The common use case is to use the Clang
host toolchain for building unit test targets. If you do not want to use the Clang host toolchain,
the other tools should be made available as soon as possible. This was not the case in older
revisions of this project.

---

Building the Clang compiler can take some time, so have a bit of patience. It is recommended
to build all packages on a Jenkins node and upload the artifacts to a binary archive.
If you do not have the infrastructure to use or set up Jenkins, you can also use your local
workstation and upload the packages to a binary archive.

Using a binary archive has the benefit that packages only need to be built once and can then simply be downloaded from the archive instead of being built again and again from scratch. The binary archive does not necessarily have to be a server. You can also upload the artifact to local storage on your hard disk or a network drive.

The basement project is prepared to configure user-specific binary archives. As you can see at
the bottom of the `default.yaml` file, there is an `include` section:

```yaml
include:
    # optional include for user specific settings.
    # note: This file (user.yaml) is not under version control and shall be placed
    #       in the root directory of the project relative to the default.yaml.
    - user
    # optional include for user specific binary archives.
    # note: This file (archive.yaml) is not added to .gitignore and shall be placed
    #       in the root directory of the project relative to the default.yaml.
    - archive
```

For example, place the file `archive.yaml` next to `default.yaml` and add the following content:

```yaml
archive:
    -
        backend: file
        path: D:\archives\basement
        flags: [download,upload]
```

Now you have configured a local binary archive on your workstation. If you execute Bob with
the argument `--upload`, Bob will automatically upload the artifacts to `D:\archives\basement`.

```shell
# The binary archive is empty, start building all packages and upload it to the binary archive
bob dev buildall --upload
# or with additional self built clang host-toolchain
bob dev buildall -DENABLE_X86_64_CLANG_HOST_TOOLCHAIN=True --upload
...
Duration: 0:54:24.442231, 16 checkouts (0 overrides active), 27 packages built, 0 downloaded.
```

As you can see, building all packages takes approximately one hour (without the Clang host
toolchain). Now let's check whether the previously configured binary archive works:

```shell
# cleanup-up project
rm -r .\dev\
rm .bob-*
# "build" (download) again all packages
bob dev buildall
...
Duration: 0:08:47.917908, 0 checkouts (0 overrides active), 1 package built, 12 downloaded.
```

As you can see, it is now about six times faster, which is much more practical. If you have
multiple workstations that you want to work on, you can share this binary archive among all
workstations or team members. Then everyone can download the pre-built packages from there. As long
as the recipes and their inputs have not changed, Bob will always download packages from there. If a
recipe or its input has changed, Bob will not find a suitable artifact in the binary archive and will
build the affected package(s) from scratch.

In the `tests` directory, there are several recipes that build small test packages using the
basement layer. They act as smoke tests for this project.

```shell
    cd tests
    # use the default MSVC host-toolchain
    bob dev tests::cmake::greeter-host -v
    # use the clang host-toolchain
    bob dev tests::cmake::greeter-host -DENABLE_X86_64_CLANG_HOST_TOOLCHAIN=True -v
    # crosscompile the same sources with the gcc-aarch64-linux-gnu cross-toolchain
    bob dev tests::cmake::greeter-cross -v
    # build a simple code generator example
    bob dev tests::python::test -v
    # build a simple sphinx documentation
    bob dev tests::sphinx::doc -v
```

# How to use

First, you need to add the `basement` layer to your project. To do so, add a `layers` entry to
`config.yaml`:

    bobMinimumVersion: "1.3.0"
    layers:
        - basement

and then add this repository as a submodule to your project:

    $ git submodule add https://github.com/sbixl/bob.native.windows.basement.git layers/basement

To use all facilities of the basement project, you just need to inherit the `basement::rootrecipe`
class in your root recipe:

    inherit: [ "basement::rootrecipe" ]

This will make your recipe a root recipe. See the next chapter to see which tools and toolchains are
readily available.

# Provided tools and toolchains

The following tools can be used by naming them in `{checkout,build,package}Tools`:

  * 7z
  * ninja
  * cmake
  * python3

The following tools are not available by default but can be added as dependencies (see the test
examples for more information on how to do this):

  * sphinx (including PlantUML plugin)
  * doxygen
  * google-test

Since Windows does not have a native compiler by default, the MSVC compiler must be installed.
Independently of this, a native host Clang compiler can optionally be built downstream as the host
toolchain. The Clang compiler uses the GNU command line by default and not the MSVC command line.

The following cross-compiling toolchains are available pre-configured. If you need other targets,
you can depend on `devel::cross-toolchain` directly and configure it as you like.

  * `devel::cross-toolchain-gcc-aarch64-linux-gnu`: ARMv8-A AArch64 Linux with glibc.
  * `devel::cross-toolchain-gcc-arm-linux-gnueabihf`: ARMv7-A Linux with glibc. Hard
    floating point ABI.
  * `devel::cross-toolchain-gcc-arm-none-eabi`: 32-bit Arm Cortex-A,-M,-R bare metal toolchain with
    newlib libc.
  * `devel::cross-toolchain-gcc-x86_64-linux-gnu`: x86_64 toolchain for Linux with glibc.

To use a cross toolchain as well as the Clang host toolchain, include it where needed via:

    depends:
        - name: <recipe name here>
          use: [tools, environment]
          forward: True

# Continuous Integration (Bob Jenkins support for native Windows)

It is now possible to use Bob in combination with Jenkins for continuous integration (CI) while
still remaining under native Windows. The basement project is ready for CI and can be built using
distributed Jenkins nodes.

While setting up the CI infrastructure, especially the Jenkins nodes, the `JENKINS_HOME`
environment variable should always be set to a short path such as `C:\data\jenkins_home`, because
otherwise the build of some artifacts (especially the host Clang compiler) will fail because of path
limitations under native Windows.

The following example briefly shows how easy it is to configure the corresponding Jenkins jobs with
the Bob Jenkins interface. The option `-n windows` tells the Jenkins master to schedule jobs only on
build nodes tagged with the label **windows**.

```shell
    bob jenkins add local http://user@localhost:8080 --r buildall --host-platform win32 -n windows --upload
    bob jenkins set-options local --clean
    bob jenkins set-options local --download
    bob jenkins set-options local -o jobs.update=lazy
    bob jenkins push local
```

The option `--upload` tells Jenkins to copy the build artifacts to a dedicated binary archive. In my
setup, this is a simple nginx-based HTTP server located on the Jenkins master host device. In order
to tell Bob where the binary archive can be found, you have to add the following configuration to the
`default.yaml`, `user.yaml`, or `archive.yaml` file:

    archive:
        -
            backend: http
            url: "http://localhost:80"
            # default: upload and download (re-use) artifacts from artefact server

When using this project as a Bob layer in another project, the binary artifact server should also be
added to the `default.yaml` file:

    archive:
        -
            backend: http
            url: "http://localhost:80"
            # only download artifacts from artefact server, never upload any
            flags: [download]

Please take care to set the option `flags: [download]` to prevent uploading binary artifacts from the
Bob project that uses this basement layer to the artifact server unless this is explicitly desired.

# Some words about performance

Unfortunately, the build process under Windows is slower than under Linux. Especially the CMake
configure step can take several seconds to finish. There are some discussions and issues about this,
but there seems to be no real solution yet.

Here are a few tips on how to speed up the build process:

* Do not build in your user directory, because the Windows indexer, which usually runs in the
  background, can drastically increase build times (in my tests by about 50 percent).
  If you want to build in your home directory, you can configure a special directory that should be
  excluded by the indexer.
* Exclude the root directory from your antivirus program.

# Planned features

- [ ] Add example projects which use the layer
