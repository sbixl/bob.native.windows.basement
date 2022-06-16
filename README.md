# Previous note

Most of the recipes and classes included in this project were widely adopted from the [basement project](https://github.com/BobBuildTool/basement). But since the project currently only
 supports bash as shell script language, this is a attempt to introduce the pwsh script
 language to be used on native windows without msys. For this the recipes and classes were ported from bash to pwsh as far as possible.

The approach of an position independent python3 is widely adopted from the [pipython3 project](https://github.com/mahaase/pipython3). But since this project currently only supports bash as shell script language, porting to pwsh was necessary too.

# Native Windows Basement

These basement project is a collection of useful recipes and classes that can be
used by other projects. Most importantly it provides standard classes
to handle common build systems and other standard tasks. Additionally a native clang
and common GCC toolchains are ready-to-use.

# Prerequisites

* A x86_64 system with Windows 10 and some minimal tools installed
  * Visual Studio Build Tools 2019 with minimal settings:
    ![Alt text](doc/vs_build_tools_2019_setup.PNG "Visual Studio Build Tools 2019")
    Note: A full installation of the Visual Studio 2019 should be work too
  * powershell 5.x

* Windows 10 system configuration
  * Make sure you can create symbolic links without admin rights. Usually you can enable
    this by switching to the developer mode. If this does not work, enable it in your [security policy setting](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/create-symbolic-links).
  * [Enable long path support](https://www.msftnext.com/how-to-enable-ntfs-long-paths-in-windows-10/).
* Bleeding edge Bob Build Tool (https://github.com/BobBuildTool/bob)

# How to build

Take care using a flat folder structure. Regardless of whether or not long paths are enabled, if the paths are too long, the build process of the clang compiler will fail as some paths could not be resolved. The best way is to clone the repository e.g under "C:\Work" or something similar.

Since there are currently no examples that attract this project as a layer you
can clone the recipes and build them with Bob in development mode:

```shell
    git clone https://github.com/sbixl/bob.native.windows.basement.git
    cd bob.native.windows.basement
    bob dev buildall
```

Because there is currently no Jenkins / CI support for windows yet, you have
to build all packages locally in your host environment. Building the clang compiler
can take some time, so have a bit of patience. ;-)

In tests/cmake there are a couple of recipes that build small test packages which use the basement layer. They act as smoke tests for this project.

```shell
    bob dev tests::cmake::greeter-host
    bob dev tests::cmake::greeter-cross
    bob dev tests::python::test
```

# How to use

First you need to add the `basement` layer to your project. To do so add a
`layers` entry to `config.yaml`:

    bobMinimumVersion: "0.20"
    layers:
        - basement

and then add this repository as submodule to your project:

    $ git submodule add https://github.com/sbixl/bob.native.windows.basement.git layers/basement

To use all facilities of the basement project you just need to inherit the `basement::rootrecipe`
class in your root recipe:

    inherit: [ "basement::rootrecipe" ]

This will make your recipe a root recipe. See the next chapter what tools
and toolchains are readily available.

# Provided tools and toolchains

The following tools can be used by naming them in `{checkout,build,package}Tools`:

* 7z
* ninja
* cmake
* python3

Since windows does not have a native compiler by default, the msvc compiler must
be installed. Independently of this, you can build the clang compiler downstream
as host toolchain. Building the clang compiler as host toolchain is disabled by default.
If you want the clang compiler as host toolchain you can simply set `BASEMENT_HOST_CLANG_TOOLCHAIN` to "1" in the `default.yaml`. In this project
the clang compiler uses the gnu command line by default and not the msvc command line.

The following cross compiling toolchains are available pre-configured. If you need
other targets you can depend on `devel::cross-toolchain` directly and configure it
as you like.

* `devel::cross-toolchain-gcc-aarch64-linux-gnu`: ARMv8-A AArch64 Linux with glibc.
* `devel::cross-toolchain-gcc-arm-linux-gnueabihf`: ARMv7-A Linux with glibc. Hard
  floating point ABI.
* `devel::cross-toolchain-gcc-arm-none-eabi`: 32-bit Arm Cortex-A,-M,-R bare metal toolchain with
  newlib libc.
* `devel::cross-toolchain-gcc-x86_64-linux-gnu`: x86_64 toolchain for Linux with glibc.
* `devel::cross-toolchain-llvm-embedded-toolchain-for-arm`: 32-bit Arm Cortex-M bare metal toolchain with newlib libc.

To use a cross compiling toolchain include it where needed via:

    depends:
        - name: <recipe name here>
          use: [tools, environment]
          forward: True

# Some words about performance

Unfortunately the building process under windows is slower than under linux. Especially
the CMake configure step can take several seconds to finish. There are some conversations
and issue about this but there seems to be no real solution yet.

Here are a few tips how to speed up the build process:

* Do not build in your user directory because the windows indexer which usually runs
  in the background can drastically increase the build time (in my tests about 50 percent).
  If you want to build in your home directory, you can configure a special directory
  which should be excluded by the indexer.
* Exclude the root directory from your Anti virus program.

# Planned features

- [ ] Add example projects which use the layer
- [ ] Improve recipes of the clang host toolchain
- [ ] Extend tooling support (e.g. doxygen)

