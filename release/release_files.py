#!/usr/bin/env python3
import os
import re
from pathlib import Path

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = HERE + "/.."

# blacklisting is for two purposes:
# - minimizing release download size
# - keeping the diff readable
blacklist = [
  "^scripts/",
  "body/STL/",
  "tools/cabana/",
  "panda/examples/",
  "opendbc/generator/",

  "^tools/",
  "^tinygrad_repo/",

  "matlab.*.md",

  ".git$",  # for submodules
  ".git/",
  ".github/",
  ".devcontainer/",
  "Darwin/",
  ".vscode/",

  # no LFS
  ".lfsconfig",
  ".gitattributes",
]

# Sunnypilot blacklist
sunnypilot_blacklist = [
  ".idea/",
  ".run/",
  ".run/",
  "release/ci/scons_cache/",
  "system/loggerd/sunnylink_uploader.py",  # Temporarily, until we are ready to roll it out widely
  ".gitlab-ci.yml",
  ".clang-tidy",
  ".dockerignore",
  ".editorconfig",
  ".gitmodules",
  ".pre-commit-config.yaml",
  ".python-version",
  ".dockerignore",
  ".editorconfig",
  ".gitlab-ci.yml",
  ".gitmodules",
  ".pre-commit-config.yaml",
  ".python-version",
  ".dockerignore",
  ".editorconfig",
  ".gitlab-ci.yml",
  ".gitmodules",
  ".pre-commit-config.yaml",
  ".python-version",
  "body/.pre-commit-config.yaml",
  "body/board/canloader.py",
  "body/board/flash_base.sh",
  "body/board/flash_knee.sh",
  "body/board/recover.sh",
  "body/Dockerfile",
  "body/LICENSE",
  "body/pyproject.toml",
  "body/README.md",
  "body/requirements.txt",
  "body/SConstruct",
  "cereal/.dockerignore",
  "cereal/.pre-commit-config.yaml",
  "cereal/codecov.yml",
  "cereal/Dockerfile",
  "cereal/generate_javascript.sh",
  "cereal/LICENSE",
  "cereal/maptile.capnp",
  "cereal/messaging/demo.py",
  "cereal/messaging/msgq.md",
  "cereal/messaging/stress.py",
  "cereal/messaging/test_runner",
  "cereal/messaging/tests/",
  "cereal/pyproject.toml",
  "cereal/README.md",
  "cereal/SConstruct",
  "cereal/site_scons/",
  "cereal/visionipc/test_runner",
  "cereal/visionipc/tests/",
  "codecov.yml",
  "common/tests/",
  "common/transformations/.gitignore",
  "common/transformations/README.md",
  "common/transformations/tests/",
  "conftest.py",
  "Dockerfile.openpilot",
  "Dockerfile.openpilot_base",
  "docs/_static/",
  "docs/assets/",
  "docs/BOUNTIES.md",
  "docs/c_docs.rst",
  "docs/conf.py",
  "docs/index.md",
  "docs/Makefile",
  "docs/overview.rst",
  "docs/README.md",
  "docs/SAFETY.md",
  "docs/WORKFLOW.md",
  "opendbc/.pre-commit-config.yaml",
  "opendbc/bmw_e9x_e8x.dbc",
  "opendbc/cadillac_ct6_chassis.dbc",
  "opendbc/cadillac_ct6_object.dbc",
  "opendbc/cadillac_ct6_powertrain.dbc",
  "opendbc/can/tests/",
  "opendbc/chrysler_cusw.dbc",
  "opendbc/Dockerfile",
  "opendbc/ESR.dbc",
  "opendbc/ford_cgea1_2_bodycan_2011.dbc",
  "opendbc/ford_cgea1_2_ptcan_2011.dbc",
  "opendbc/ford_fusion_2018_pt.dbc",
  "opendbc/gm_global_a_high_voltage_management.dbc",
  "opendbc/gm_global_a_lowspeed_1818125.dbc",
  "opendbc/gm_global_a_lowspeed.dbc",
  "opendbc/gm_global_a_powertrain_expansion.dbc",
  "opendbc/honda_fit_hybrid_2018_can_generated.dbc",
  "opendbc/honda_pilot_2023_can_generated.dbc",
  "opendbc/hyundai_2015_ccan.dbc",
  "opendbc/hyundai_2015_mcan.dbc",
  "opendbc/hyundai_i30_2014.dbc",
  "opendbc/hyundai_kia_mando_corner_radar_generated.dbc",
  "opendbc/hyundai_santafe_2007.dbc",
  "opendbc/LICENSE",
  "opendbc/luxgen_s5_2015.dbc",
  "opendbc/mazda_3_2019.dbc",
  "opendbc/mazda_radar.dbc",
  "opendbc/mazda_rx8.dbc",
  "opendbc/mercedes_benz_e350_2010.dbc",
  "opendbc/nissan_xterra_2011.dbc",
  "opendbc/opel_omega_2001.dbc",
  "opendbc/pyproject.toml",
  "opendbc/README.md",
  "opendbc/requirements.txt",
  "opendbc/SConstruct",
  "opendbc/site_scons/",
  "opendbc/tesla_model3_party.dbc",
  "opendbc/tesla_model3_vehicle.dbc",
  "opendbc/toyota_2017_ref_pt.dbc",
  "opendbc/toyota_iQ_2009_can.dbc",
  "opendbc/toyota_prius_2010_pt.dbc",
  "opendbc/toyota_radar_dsu_tssp.dbc",
  "opendbc/volvo_v40_2017_pt.dbc",
  "opendbc/volvo_v60_2015_pt.dbc",
  "panda/.pre-commit-config.yaml",
  "panda/Dockerfile",
  "panda/docs/",
  "panda/drivers/",
  "panda/LICENSE",
  "panda/mypy.ini",
  "panda/panda.png",
  "panda/pyproject.toml",
  "panda/README.md",
  "panda/requirements.txt",
  "panda/SConstruct",
  "panda/setup.cfg",
  "panda/setup.py",
  "panda/tests/",
  "poetry.lock",
  "rednose_repo/.dockerignore",
  "rednose_repo/.editorconfig",
  "rednose_repo/.gitignore",
  "rednose_repo/.pre-commit-config.yaml",
  "rednose_repo/Dockerfile",
  "rednose_repo/examples/",
  "rednose_repo/LICENSE",
  "rednose_repo/pyproject.toml",
  "rednose_repo/README.md",
  "rednose_repo/rednose/",
  "SECURITY.md",
  "selfdrive/assets/compress-images.sh",
  "selfdrive/assets/strip-svg-metadata.sh",
  "selfdrive/boardd/tests/__init__.py",
  "selfdrive/boardd/tests/bootstub.panda_h7_spiv0.bin",
  "selfdrive/boardd/tests/bootstub.panda_h7.bin",
  "selfdrive/boardd/tests/bootstub.panda.bin",
  "selfdrive/boardd/tests/test_boardd_spi.py",
  "selfdrive/boardd/tests/test_boardd_usbprotocol",
  "selfdrive/boardd/tests/test_pandad.py",
  "selfdrive/car/CARS_template.md",
  "selfdrive/car/docs.py",
  "selfdrive/car/ford/tests/",
  "selfdrive/car/gm/tests/",
  "selfdrive/car/honda/tests/",
  "selfdrive/car/hyundai/tests/",
  "selfdrive/car/README.md",
  "selfdrive/car/subaru/tests/",
  "selfdrive/car/tests/.gitignore",
  "selfdrive/car/tests/big_cars_test.sh",
  "selfdrive/car/tests/routes.py",
  "selfdrive/car/tests/test_can_fingerprint.py",
  "selfdrive/car/tests/test_docs.py",
  "selfdrive/car/tests/test_fingerprints.py",
  "selfdrive/car/tests/test_fw_fingerprint.py",
  "selfdrive/car/tests/test_lateral_limits.py",
  "selfdrive/car/tests/test_models_segs.txt",
  "selfdrive/car/tests/test_models.py",
  "selfdrive/car/tests/test_platform_configs.py",
  "selfdrive/car/toyota/tests/",
  "selfdrive/car/volkswagen/tests/",
  "selfdrive/controls/.gitignore",
  "selfdrive/controls/lib/sunnypilot/tests/",
  "selfdrive/controls/lib/tests/",
  "selfdrive/controls/tests/",
  "selfdrive/debug/__init__.py",
  "selfdrive/debug/adb.sh",
  "selfdrive/debug/can_print_changes.py",
  "selfdrive/debug/can_table.py",
  "selfdrive/debug/check_can_parser_performance.py",
  "selfdrive/debug/check_lag.py",
  "selfdrive/debug/check_timings.py",
  "selfdrive/debug/clear_dtc.py",
  "selfdrive/debug/count_events.py",
  "selfdrive/debug/cpu_usage_stat.py",
  "selfdrive/debug/cycle_alerts.py",
  "selfdrive/debug/debug_fw_fingerprinting_offline.py",
  "selfdrive/debug/dump_car_docs.py",
  "selfdrive/debug/fingerprint_from_route.py",
  "selfdrive/debug/internal/",
  "selfdrive/debug/live_cpu_and_temp.py",
  "selfdrive/debug/print_docs_diff.py",
  "selfdrive/debug/print_flags.py",
  "selfdrive/debug/read_dtc_status.py",
  "selfdrive/debug/README.md",
  "selfdrive/debug/run_process_on_route.py",
  "selfdrive/debug/set_car_params.py",
  "selfdrive/debug/show_matching_cars.py",
  "selfdrive/debug/test_fw_query_on_routes.py",
  "selfdrive/debug/toyota_eps_factor.py",
  "selfdrive/locationd/test/",
  "selfdrive/modeld/models/dmonitoring_model.current",
  "selfdrive/modeld/models/dmonitoring_model.onnx",
  "selfdrive/modeld/models/README.md",
  "selfdrive/modeld/tests/",
  "selfdrive/modeld/thneed/README",
  "selfdrive/monitoring/helpers.py",
  "selfdrive/monitoring/README.md",
  "selfdrive/monitoring/test_hands_monitoring.py",
  "selfdrive/monitoring/test_monitoring.py",
  "selfdrive/test/.gitignore",
  "selfdrive/test/ci_shell.sh",
  "selfdrive/test/ciui.py",
  "selfdrive/test/cpp_harness.py",
  "selfdrive/test/docker_build.sh",
  "selfdrive/test/docker_common.sh",
  "selfdrive/test/docker_tag_multiarch.sh",
  "selfdrive/test/longitudinal_maneuvers/",
  "selfdrive/test/loop_until_fail.sh",
  "selfdrive/test/process_replay/",
  "selfdrive/test/profiling/",
  "selfdrive/test/scons_build_test.sh",
  "selfdrive/test/setup_vsound.sh",
  "selfdrive/test/setup_xvfb.sh",
  "selfdrive/test/test_updated.py",
  "selfdrive/test/update_ci_routes.py",
  "selfdrive/ui/__init__.py",
  "selfdrive/ui/installer/",
  "selfdrive/ui/mui",
  "selfdrive/ui/qt/python_helpers.py",
  "selfdrive/ui/qt/setup/reset",
  "selfdrive/ui/qt/setup/setup",
  "selfdrive/ui/qt/setup/updater",
  "selfdrive/ui/tests/__init__.py",
  "selfdrive/ui/tests/.gitignore",
  "selfdrive/ui/tests/body.py",
  "selfdrive/ui/tests/create_test_translations.sh",
  "selfdrive/ui/tests/cycle_offroad_alerts.py",
  "selfdrive/ui/tests/test_soundd.py",
  "selfdrive/ui/tests/test_ui/",
  "selfdrive/ui/tests/ui_snapshot",
  "selfdrive/ui/translations/auto_translate.py",
  "selfdrive/ui/translations/create_badges.py",
  "selfdrive/ui/translations/README.md",
  "selfdrive/ui/ui.py",
  "selfdrive/ui/watch3",
  "teleoprtc_repo/",
  "teleoprtc_repo/.gitignore",
  "teleoprtc_repo/.pre-commit-config.yaml",
  "teleoprtc_repo/examples/",
  "teleoprtc_repo/LICENSE",
  "teleoprtc_repo/pyproject.toml",
  "teleoprtc_repo/README.md",
  "teleoprtc_repo/scripts/",
  "teleoprtc_repo/teleoprtc/",
  "teleoprtc_repo/tests/",
  "third_party/acados/acados_template/.gitignore",
  "third_party/acados/build.sh",
  "third_party/acados/x86_64/",
  "third_party/bootstrap/.gitignore",
  "third_party/catch2/",
  "third_party/libyuv/.gitignore",
  "third_party/libyuv/build.sh",
  "third_party/libyuv/LICENSE",
  "third_party/libyuv/x86_64/",
  "third_party/maplibre-native-qt/.gitignore",
  "third_party/snpe/x86_64-linux-clang/",
  "tinygrad_repo/tinygrad/renderer/cuda.py",
  "tinygrad_repo/tinygrad/renderer/llvmir.py",
  "tinygrad_repo/tinygrad/renderer/metal.py",
  "tinygrad_repo/tinygrad/renderer/triton.py",
  "tinygrad_repo/tinygrad/renderer/wgsl.py",
  "tinygrad_repo/tinygrad/runtime/ops_clang.py",
  "tinygrad_repo/tinygrad/runtime/ops_cuda.py",
  "tinygrad_repo/tinygrad/runtime/ops_hip.py",
  "tinygrad_repo/tinygrad/runtime/ops_llvm.py",
  "tinygrad_repo/tinygrad/runtime/ops_metal.py",
  "tinygrad_repo/tinygrad/runtime/ops_shm.py",
  "tinygrad_repo/tinygrad/runtime/ops_torch.py",
  "tinygrad_repo/tinygrad/runtime/ops_webgpu.py",
]

# Merge the blacklists
blacklist += sunnypilot_blacklist

# gets you through the blacklist
whitelist = [
  "^tools/lib/(?!.*__pycache__).*$",
  "tools/bodyteleop/",

  "tinygrad_repo/openpilot/compile2.py",
  "tinygrad_repo/extra/onnx.py",
  "tinygrad_repo/extra/onnx_ops.py",
  "tinygrad_repo/extra/thneed.py",
  "tinygrad_repo/extra/utils.py",
  "tinygrad_repo/tinygrad/codegen/kernel.py",
  "tinygrad_repo/tinygrad/codegen/linearizer.py",
  "tinygrad_repo/tinygrad/features/image.py",
  "tinygrad_repo/tinygrad/features/search.py",
  "tinygrad_repo/tinygrad/nn/*",
  "tinygrad_repo/tinygrad/renderer/cstyle.py",
  "tinygrad_repo/tinygrad/renderer/opencl.py",
  "tinygrad_repo/tinygrad/runtime/lib.py",
  "tinygrad_repo/tinygrad/runtime/ops_cpu.py",
  "tinygrad_repo/tinygrad/runtime/ops_disk.py",
  "tinygrad_repo/tinygrad/runtime/ops_gpu.py",
  "tinygrad_repo/tinygrad/shape/*",
  "tinygrad_repo/tinygrad/.*.py",
]

if __name__ == "__main__":
  for f in Path(ROOT).rglob("**/*"):
    if not (f.is_file() or f.is_symlink()):
      continue

    rf = str(f.relative_to(ROOT))
    blacklisted = any(re.search(p, rf) for p in blacklist)
    whitelisted = any(re.search(p, rf) for p in whitelist)
    if blacklisted and not whitelisted:
      continue

    print(rf)
