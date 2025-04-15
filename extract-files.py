#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

    namespace_imports = [
    'device/xiaomi/topaz',
    'hardware/xiaomi',
    'hardware/qcom/audio',
    'hardware/qcom/display',
    'hardware/qcom/media',
    'vendor/qcom/opensource/agm',
    'vendor/qcom/opensource/data-ipa-cfg-mgr',
    'vendor/qcom/opensource/dataipa',
    'vendor/xiaomi/topaz',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

blob_fixups: blob_fixups_user_type = {
    ('vendor/bin/hw/android.hardware.security.keymint-service-qti', 'vendor/lib64/libqtikeymint.so'): blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'vendor/etc/init/init.batterysecret.rc': blob_fixup()
        .replace('on charger', 'on property:init.svc.vendor.charger=running'),
    'vendor/etc/init/init.mi_thermald.rc': blob_fixup()
        .replace('on charger', 'on property:init.svc.vendor.charger=running'),
    'vendor/etc/seccomp_policy/c2audio.vendor.ext-arm64.policy': blob_fixup()
        .add_line_if_not_present('setsockopt: 1'),
    'vendor/lib64/libqcrilNr.so': blob_fixup()
        .replace('persist.vendor.radio.poweron_opt', 'persist.vendor.radio.poweron_ign'),
    'vendor/lib64/libril-db.so': blob_fixup()
        .replace('persist.vendor.radio.poweron_opt', 'persist.vendor.radio.poweron_ign'),
    'vendor/bin/STFlashTool': blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
}

module = ExtractUtilsModule(
    'topaz',
    'xiaomi',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
