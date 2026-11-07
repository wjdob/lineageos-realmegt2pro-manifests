# LineageOS 24.0 source for Realme GT2 Pro

Pinned Android 17 sources for **Native25**, with RMX3301 device/common
repositories and the remaining framework patches.

[Downloads and install guide](https://github.com/wjdob/lineageos-realmegt2pro/tree/lineage-24.0) |
[Kernel source and credits](https://github.com/wjdob/lineageos-realmegt2pro/blob/lineage-24.0/SOURCES.md) |
[Optional-app source](https://github.com/wjdob/realmegt2pro-oem-apps/tree/lineage-24.0)

The commands below cover source download and patch preparation. A complete rebuild
using these component manifests has not yet been tested. Stock-file preparation
and release signing still require manual setup; a complete public build guide is pending.

## Requirements

- Linux with Git, Google's `repo` tool, Python 3.12 and `patch`.
- Enough storage for an Android source checkout and build output.
- Your own matching `RMX3301_15.0.0.1410(EX01)` stock files and signing keys.
- The Android build tools downloaded by the pinned manifest.

`integration/configs/` lists expected stock-file hashes. `lineage-24.0-vendor-inputs.json` and `lineage-24.0-vendor-output.json` describe the Ferrari vendor files; `common-runtime-24.0.json` lists additional common runtime files.
The original [release source kit](https://github.com/wjdob/lineageos-realmegt2pro/tree/lineage-24.0/source/lineage-24.0)
contains the extraction/build tools and configurations used for the release.
Proprietary files and private keys are supplied separately.

## Download source

Start in an empty Android source directory. These commands select the release tag:

```sh
repo init -u https://github.com/wjdob/lineageos-realmegt2pro-manifests.git -b source-native25-20261107
repo sync -c -j4
git clone --branch source-native25-20261107 https://github.com/wjdob/lineageos-realmegt2pro-manifests.git ../rmx3301-source
python ../rmx3301-source/tools/validate_layout.py
```

For development, use `lineage-24.0` instead of the source tag. `default.xml` lists
the exact versions of every project. `upstream.xml` contains the original versions
before the project's patches.

## Prepare remaining patches

The device/common repositories already include their release fixes. The patches
in `integration/recipe.json` apply to the remaining projects.

Provide the matching stock files and source versions first. Private template paths
listed in `source-layout.json` are relative to `integration/`; place your files there.
Then run from the Android source directory:

```sh
python ../rmx3301-source/tools/prepare_patches.py --tree "$PWD" --output /tmp/rmx3301-source-stage
```

The script checks device/common versions and file hashes. It writes the remaining
patched files into a new staging directory and leaves the Android checkout unchanged.
An existing output directory or mismatched input causes an error. Inspect the
staged files before copying them into your build checkout.

Use this recipe with `default.xml`. The original full recipe is for `upstream.xml`;
applying it to the component forks would apply device/common patches twice.

The release uses product **`lineage_ferrari`**, kernel **5.10.246** and target release **`cp2a`**.
Stock runtime files and signing setup must be complete before building an OTA.

## Credits and contributions

Based on pjgowtham's device/common/kernel work, LineageOS/AOSP and upstream
contributors. Original licenses and copyright notices remain in place.
Submit manifest/patch changes here. Report phone problems through the
[release issue forms](https://github.com/wjdob/lineageos-realmegt2pro/issues/new/choose).
