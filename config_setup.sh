#!/usr/bin/env bash
#利用scripts/config对内核进行修改，之后需要写个注释对上述提到的所以东西进行讲解
scripts/config --disable DEBUG_INFO_X86
scripts/config --disable DEBUG_INFO_VMCORE
scripts/config --disable DEBUG_INFO_SPLIT
scripts/config --disable DEBUG_INFO_BTF_MODULES
scripts/config --disable DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
scripts/config --disable DEBUG_INFO_PERF
scripts/config --disable DEBUG_INFO_BTF
scripts/config --disable DEBUG_INFO_DWARF4
scripts/config --disable DEBUG_INFO_REDUCED
scripts/config --set-str SYSTEM_TRUSTED_KEYS "" 
scripts/config --set-str SYSTEM_REVOCATION_KEYS "" 
scripts/config --undefine DEBUG_INFO 
scripts/config --undefine DEBUG_INFO_COMPRESSED 
scripts/config --undefine DEBUG_INFO_REDUCED 
scripts/config --undefine DEBUG_INFO_SPLIT 
scripts/config --undefine GDB_SCRIPTS 
scripts/config --set-val DEBUG_INFO_DWARF5 n 
scripts/config --set-val DEBUG_INFO_NONE y 
:<<EOF
# 支持2.4G无线键盘
# <*> USB HID transport layer
scripts/config -e CONFIG_USB_HID
# 提高桌面响应速度
# (X) Preemptible Kernel (Low-Latency Desktop) [CONFIG_PREEMPT]
scripts/config -e CONFIG_PREEMPT
# (X) Idle dynticks system (tickless idle) [CONFIG_NO_HZ_IDLE]
scripts/config -e CONFIG_NO_HZ_IDLE
# (X) Simple tick based cputime accounting [CONFIG_TICK_CPU_ACCOUNTING]
scripts/config -e CONFIG_TICK_CPU_ACCOUNTING
# 桌面系统的“鸡血补丁”，开启后能显著降低操作延迟、提升程序响应速度
# [*] Automatic process group schedulin [CONFIG_SCHED_AUTOGROUP]
scripts/config -e CONFIG_SCHED_AUTOGROUP
EOF