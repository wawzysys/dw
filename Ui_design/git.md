如果你想在你的 Git 仓库中执行类似的命令来获取特定文件的差异（diff），你可以使用下面的命令来查看两个版本之间的差异或者是与上一个提交的差异。

### 查看两个提交之间的文件差异

如果你已经知道想比较的两个提交的哈希值，你可以使用如下命令：

```bash
git diff COMMIT_HASH1 COMMIT_HASH2 -- Ui_design/main_test.py
```

将 `COMMIT_HASH1` 和 `COMMIT_HASH2` 替换为你想比较的具体提交哈希值。

### 查看文件的最近更改

如果你只想查看文件相对于上次提交的改动，可以使用：

```bash
git diff HEAD^ HEAD -- Ui_design/main_test.py
```

这会显示从上一次提交到当前最新提交（HEAD）之间的差异。

### 查看某次提交对文件的改动

如果你想看某个特定提交对该文件的改动，可以使用 `git show` 命令：

```bash
git show COMMIT_HASH -- Ui_design/main_test.py
```

这条命令会显示在 `COMMIT_HASH` 中，`Ui_design/main_test.py` 文件的具体修改内容。

### 获取特定提交之后的文件差异

如果你想看从某个特定提交之后该文件的所有变化，可以使用：

```bash
git diff COMMIT_HASH..HEAD -- Ui_design/main_test.py
```

这里的 `COMMIT_HASH` 是你关注的特定提交，`HEAD` 表示当前分支的最新提交。

确保你在执行这些命令前处于 Git 仓库的根目录，或者确保你的路径指向正确的仓库位置。这样你就可以正确地访问到文件并获取到差异信息。