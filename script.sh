#!/bin/bash
current_time=$(date +"%Y-%m-%d %H:%M:%S")

git config user.name "XXTXTOP"
git config user.email "xxtxtop@gmail.com"

# 追加当前时间到文件
echo "$current_time" >> time.txt

# 删除第一行
sed -i '1d' time.txt


git add *.txt create_file.sh get_latest_kernel.py script.sh time.py time.txt

# 从time.txt文件中获取最后一行
commit_message=$(tail -n 1 time.txt)

# 设置GIT_EDITOR环境变量为"true"，以避免打开编辑器
export GIT_EDITOR=true

# 提交代码并添加提交消息
echo "$commit_message" | git commit -F - --no-edit

# 推送提交到远程仓库
git pull 
echo "$commit_message" | git commit -F - --no-edit
git push 
# 检查git命令的返回状态
if [ $? -eq 0 ]; then
    echo "Git push successful."
else
    echo "Git push failed."
fi
