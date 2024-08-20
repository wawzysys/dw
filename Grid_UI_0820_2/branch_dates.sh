#!/bin/bash

# 确保在 Git 仓库目录中运行
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "当前目录不是 Git 仓库！"
    exit 1
fi

echo "各分支最后提交信息如下："
# 遍历所有分支的名字，包括处理带星号的当前分支
for branch in $(git branch --format "%(refname:short)" | sed 's/^\* //'); do
    # 使用 git show 查看每个分支的最后提交信息
    echo -n "$branch: "
    git show --format="%ci" $branch | head -n 1
done
