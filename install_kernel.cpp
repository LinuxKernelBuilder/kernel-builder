#include <iostream>
#include <fstream>
#include <cstdlib>
#include <filesystem>
#include <unistd.h>

namespace fs = std::filesystem;

bool fileExists(const std::string& fileName) {
    return std::filesystem::exists(fileName);
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

    // 从文件读取内核下载链接
    std::ifstream file("/tmp/longtermurl.txt");
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open /tmp/longtermurl.txt" << std::endl;
        return 1;
    }

    std::string kernelUrl;
    std::getline(file, kernelUrl);
    file.close();

    // 获取下载文件名
    size_t lastSlash = kernelUrl.find_last_of('/');
    std::string fileName = kernelUrl.substr(lastSlash + 1);

    // 检查文件是否已经存在
    if (!fileExists(fileName)) {
        // 文件不存在，进行下载
        // 下载内核源代码
        std::string downloadCommand = "curl -O " + kernelUrl;
        int downloadResult = system(downloadCommand.c_str());
        if (downloadResult != 0) {
            std::cerr << "Error: Unable to download kernel source code" << std::endl;
            return 1;
        }
    } else {
        // 文件已经存在，输出提示信息
        std::cout << "Kernel source code file already exists: " << fileName << std::endl;
    }

    // ... 其余代码不变 ...

    return 0;
}
