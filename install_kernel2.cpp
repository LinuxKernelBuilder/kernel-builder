#include <iostream>
#include <fstream>
#include <cstdlib>
#include <filesystem>
#include <unistd.h>

namespace fs = std::filesystem;

int compileKernel(const std::string& versionFolder, const std::string& versionFileName) {
    // 构建文件路径
    std::string fullPath = versionFolder + "/" + versionFileName;

    // 从文件读取内核下载链接
    std::ifstream file(fullPath);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open " << fullPath << std::endl;
        return 1;
    }

    std::string kernelUrl;
    std::getline(file, kernelUrl);
    file.close();

    // 下载内核源代码
    std::string downloadCommand = "curl -O " + kernelUrl;
    int downloadResult = system(downloadCommand.c_str());
    if (downloadResult != 0) {
        std::cerr << "Error: Unable to download kernel source code" << std::endl;
        return 1;
    }

    // 获取下载文件名
    size_t lastSlash = kernelUrl.find_last_of('/');
    std::string fileName = kernelUrl.substr(lastSlash + 1);

    // 输出一些信息以便调试
    std::cout << "Downloaded kernel source code: " << fileName << std::endl;

    // 解压缩内核源代码
    std::string extractCommand = "tar -xvf " + fileName;
    int extractResult = system(extractCommand.c_str());
    if (extractResult != 0) {
        std::cerr << "Error: Unable to extract kernel source code" << std::endl;
        return 1;
    }

    // 输出一些信息以便调试
    std::string kernelDir = fileName.substr(0, fileName.find_last_of('.'));
    std::cout << "Extracted kernel source code: " << kernelDir << std::endl;

    // 进入解压缩后的目录
    chdir(kernelDir.c_str());

    // 拷贝启动目录到源代码目录
    system("cp -v /boot/config-$(uname -r) .config");

    // 额外的配置命令
    system("scripts/config --set-str SYSTEM_TRUSTED_KEYS \"\"");
    system("scripts/config --set-str SYSTEM_REVOCATION_KEYS \"\"");
    system("scripts/config --undefine DEBUG_INFO");
    system("scripts/config --undefine DEBUG_INFO_COMPRESSED");
    system("scripts/config --undefine DEBUG_INFO_REDUCED");
    system("scripts/config --undefine DEBUG_INFO_SPLIT");
    system("scripts/config --undefine GDB_SCRIPTS");
    system("scripts/config --set-val DEBUG_INFO_DWARF5 n");
    system("scripts/config --set-val DEBUG_INFO_NONE y");

    // 使用 CPU 核心数量进行并行编译
    int cpuCores = std::atoi(std::getenv("CPU_CORES"));
    std::string compileCommand = "sudo make bindeb-pkg -j" + std::to_string(cpuCores);
    int compileResult = system(compileCommand.c_str());
    if (compileResult != 0) {
        std::cerr << "Error: Compilation failed" << std::endl;
        return 1;
    }

    // 安装当前目录下所有的 Debian 包
    for (const auto& entry : fs::directory_iterator(".")) {
        if (entry.path().extension() == ".deb") {
            std::string installCommand = "sudo dpkg -i " + entry.path().filename().string();
            int installResult = system(installCommand.c_str());
            if (installResult != 0) {
                std::cerr << "Error: Installation of Debian packages failed" << std::endl;
                return 1;
            }
        }
    }

    // 更新引导
    system("sudo update-grub");

    return 0;
}

int main() {
    // 执行 Python 脚本获取最新版本和 URL
    for (int i = 0; i <= 2; ++i) {
        std::string pythonScript = "python3 get-newest-version.py " + std::to_string(i);
        int pythonExitCode = system(pythonScript.c_str());
        if (pythonExitCode != 0) {
            std::cerr << "Error: Failed to run Python script" << std::endl;
            return 1;
        }
    }

    const std::vector<std::string> versionFileNames = {
        "longtermurl.txt",
        "mainlineurl.txt",
        "stableurl.txt"
    };

    for (const auto& versionFileName : versionFileNames) {
        int compileResult = compileKernel("/tmp", versionFileName);
        if (compileResult != 0) {
            std::cerr << "Error: Compilation failed for version: " << versionFileName << std::endl;
            return 1;
        }
    }

    return 0;
}
