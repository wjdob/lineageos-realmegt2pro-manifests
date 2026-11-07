# RMX3301 LineageOS 23.2 sources

Pinned source graph for Package-23b. The device and SM8450 common trees
retain pjgowtham's history and commit the project's released integration changes.
Other framework/platform changes remain a bounded patch series in `integration/`.

[Downloads, installation and user reports](https://github.com/wjdob/lineageos-realmegt2pro/tree/lineage-23.2).
[Optional Camera, Photos and Clock source](https://github.com/wjdob/realmegt2pro-oem-apps).
Use source-repository PRs for code changes. Report phone issues through the release hub.

## Get the source

Use Linux, the Android build prerequisites and Python3.12. In a new Android directory:

```sh
repo init -u https://github.com/wjdob/lineageos-realmegt2pro-manifests.git -b lineage-23.2
repo sync -c -j4
git clone -b lineage-23.2 https://github.com/wjdob/lineageos-realmegt2pro-manifests.git device-source
python device-source/tools/validate_layout.py
```

`default.xml` pins both project forks and every upstream project by full commit.
`upstream.xml` retains the original pre-patch source graph for historical reproduction.
Use a release tag when exact repeatability is needed; version branches can advance.

## Prepare a build

Obtain your own matching .1410 stock inputs and signing identity. Device/common
extraction scripts and the contracts in `integration/configs/` describe the required
cohort. Proprietary vendor supplements and keys are outside this repository.
`source-layout.json` lists any additional private template inputs by hash; place
your own matching files under the indicated `integration/.local/` paths.
The published source kit linked from the release hub retains the original full
recipe, vendor-materialization tools and hashes for that historical build.

With the required preimage inputs present, stage the remaining changes:

```sh
python device-source/tools/prepare_patches.py --tree "$PWD" --output /tmp/rmx3301-source-stage
```

The command verifies both fork revisions and source hashes, then reconstructs only
the remaining patches into a new output directory. It leaves the input checkout
unchanged. Review the staged files and copy them into the disposable build tree.
Apply the stock-input contracts before building; the manifest alone is insufficient.
Then use the pinned build environment and `lineage_ferrari` product. Use the Android16 release configuration recorded in the original build recipe.

The two component forks already contain their changes. Reapplying the original
full recipe to them would apply those patches twice. Use `integration/recipe.json`
with this manifest; use the original recipe with `upstream.xml`.

## Scope and credits

LineageOS/AOSP and pjgowtham provide the source foundation. Existing authorship,
licenses and notices remain. `source-layout.json` records the release source
binding and verifies that all original recipe paths are represented exactly once.
Unchanged kernel projects stay pinned upstream; the release supplies their complete
source/configuration archive. Kernel DTS changes remain in the residual patch set.

This is a source reorganization. Source equivalence checks do not establish a new
native build, fresh installation or device acceptance. The existing releases and
their documented test limits remain unchanged.
