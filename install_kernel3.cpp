#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <thread>
#include <filesystem>

namespace fs = std::filesystem;

std::string find_kernel_directory(const fs::path& search_path) {
    for (const auto& entry : fs::recursive_directory_iterator(search_path)) {
        if (entry.is_directory()) {
            // 检查目录中是否有Makefile和Kconfig文件
            if (fs::exists(entry.path() / "Makefile") && fs::exists(entry.path() / "Kconfig")) {
                return entry.path().filename().string();
            }
        }
    }
    return std::string(); // 如果没有找到，返回空字符串
}

int main() {
    std::string url;
    std::ifstream file("txt/longterm.txt");

    // 从txt/longterm.txt中读取URL
    if (file.is_open() && std::getline(file, url)) {
        file.close();

        // 使用wget下载文件
        std::string wget_command = "wget -q " + url + " -O kernel.tar.xz";
        std::system(wget_command.c_str());

        // 解压文件
        std::system("tar -xf kernel.tar.xz");

        // 获取解压后的内核目录名
        std::string kernel_dir = find_kernel_directory(".");
        if (kernel_dir.empty()) {
            std::cerr << "Kernel directory not found." << std::endl;
            return 1; // 错误处理
        }

        // 进入解压后的目录并执行配置命令
        std::string config_command = "cd " + kernel_dir + " && " +
                                     "scripts/config --set-str SYSTEM_TRUSTED_KEYS \"\" && " +
                                     "scripts/config --set-str SYSTEM_REVOCATION_KEYS \"\" && " +
                                     "scripts/config --undefine DEBUG_INFO && " +
                                     "scripts/config --undefine DEBUG_INFO_COMPRESSED && " +
                                     "scripts/config --undefine DEBUG_INFO_REDUCED && " +
                                     "scripts/config --undefine DEBUG_INFO_SPLIT && " +
                                     "scripts/config --undefine GDB_SCRIPTS && " +
                                     "scripts/config --set-val DEBUG_INFO_DWARF5 n && " +
                                     "scripts/config --set-val DEBUG_INFO_NONE y";
        std::system(config_command.c_str());

        // 获取CPU核心数
        unsigned int numCPU = std::thread::hardware_concurrency();
        unsigned int halfCPU = numCPU / 2; // 使用一半的CPU核心

        // 编译内核
        std::string make_command = "cd " + kernel_dir + " && " +
                                   "make -j" + std::to_string(halfCPU) + " bindeb-pkg";
        std::system(make_command.c_str());

        // 安装所有.deb包
        std::string install_command = "cd " + kernel_dir + " && " +
                                      "sudo dpkg -i ../*.deb";
        std::system(install_command.c_str());
    } else {
        std::cerr << "Unable to open txt/longterm.txt or read URL." << std::endl;
        return 1;
    }

    return 0;
}
