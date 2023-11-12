# kernel_deb_builder

利用 GitHub Actions 自动编译 Linux 内核为 deb 包。

![1689432126348](image/README/1689432126348.png)

此架构图已经不适应目前的情况，后续需要对其进行修改，建议以代码逻辑为准。
#### 备忘录：
使用install_kernel.cpp文件通过执行

``` g++ -o install_kernel install_kernel.cpp -lstdc++fs -static-libstdc++  ``` 

来编译出install_kernel 文件，并实现本地的编译（尝试使用静态链接库而不是动态链接库），目前还未测试通过


# 如何使用

如果您想要利用我的这个自动化脚本根据自己的需求编译内核，请参考如下步骤：

#### 1. Fork 仓库

访问 [XXTX-TOP/Linux-kernel_deb_builder (github.com)](https://github.com/XXTX-TOP/Linux-kernel_deb_builder)，点击右上角的 `Fork` 按钮，并 clone 到本地

#### 2. 更新 config 文件

在本地将您获取的 config 文件替换根目录下的 `config`，可以从您系统的 `/boot/config*` 文件复制，或者手动编辑

#### 3. 编写自定义修改脚本

当前 `/patch.d/` 目录下的修改脚本是只针对我自己的需求编写的，建议您先将其删掉，然后编写自己的脚本放在这个目录下，在脚本执行过程中会自动应用该目录下的所有脚本

#### 4. 推送修改

推送后，action 自动触发，可以在您的仓库页面的 `Actions` 选项卡查看进度详情。

#### 5.下载解压安装

在您的仓库页面的 `Actions`里面下载[artifact](https://github.com/XXTX-TOP/Linux-kernel_deb_builder/suites/13914141709/artifacts/774503646) 【示例】，然后解压安装后通过sudo dpkg -i +包名 即可

#### 6、自动编译流程

流程大概是：
一、自动化处理流程，二十四小时检测Linux内核官网有没有发布新版本的内核，发布新版本的内核就和之前一个版本进行对比，新的化，就自动开始编译并打包。
二、手动触发流程，我手动点击获取按钮、如果检测到内核比我本机的内核新，那么就自动开始编译，编译完成后自动进行下载、安装、重启。PS：本机特指我用来测试的机器和虚拟机。

后续待实现流程：定制化编译、多架构编译、测试完成后一件进行签名并发布至apt源，并更新内核说明，供大家进行下载测试。

#### 7、后续发展计划

备忘录：写一个管理我方内核的工具，至少包括安装卸载指定版本，以及删除所有我方内核、删除所有除我方内核。

#### 8、依赖

| 组件        | 官网                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| wget        | [Wget - GNU Project - Free Software Foundation](https://www.gnu.org/software/wget/)                                               |
| xz-utils    | [XZ Utils (tukaani.org)](https://tukaani.org/xz/)                                                                                 |
| make        | [Make - GNU Project - Free Software Foundation](https://www.gnu.org/software/make/)                                               |
| gcc         | [GCC, the GNU Compiler Collection - GNU Project](https://gcc.gnu.org/)                                                            |
| flex        | [westes/flex: The Fast Lexical Analyzer - scanner generator for lexing in C and C++ (github.com)](https://github.com/westes/flex) |
| bison       | [Bison - GNU Project - Free Software Foundation](https://www.gnu.org/software/bison/)                                             |
| dpkg-dev    | [Dpkg — Debian Package Manager](https://www.dpkg.org/)                                                                           |
| bc          | [bc - GNU Project - Free Software Foundation](https://www.gnu.org/software/bc/)                                                   |
| rsync       | [rsync (samba.org)](https://rsync.samba.org/)                                                                                     |
| kmod        |                                                                                                                                |
| cpio        | [Cpio - GNU Project - Free Software Foundation](https://www.gnu.org/software/cpio/)                                               |
| libssl-dev  | [openssl/openssl: TLS/SSL and crypto library (github.com)](https://github.com/openssl/openssl)                                    |
| git         | [Git - Downloading Package (git-scm.com)](https://git-scm.com/download/win)                                                       |
| lsb         | [LSB Specifications (linuxfoundation.org)](https://refspecs.linuxfoundation.org/lsb.shtml)                                        |
| vim         | [welcome home : vim online](https://www.vim.org/)                                                                                 |
| libelf-dev  |                                                                                                                                |
| python3-pip | [pip · PyPI](https://pypi.org/project/pip/)                                                                                      |
| python3-tk  | [tkinter — Python interface to Tcl/Tk — Python 3.11.4 documentation](https://docs.python.org/3/library/tkinter.html)            |
| debhelper   | [debhelper(7) — debhelper — Debian jessie — Debian Manpages](https://manpages.debian.org/jessie/debhelper/debhelper.7.en.html) |

# 本项目由JetBrains提供编程软件支持：
![JetBrains Logo (Main) logo](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png)
Copyright © 2000-2023 JetBrains s.r.o. JetBrains and the JetBrains logo are registered trademarks of JetBrains s.r.o.