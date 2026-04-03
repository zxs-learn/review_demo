# review demo


…or create a new repository on the command line

echo "# review_demo" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/zxs-learn/review_demo.git
git push -u origin main

…or push an existing repository from the command line

git remote add origin https://github.com/zxs-learn/review_demo.git
git branch -M main
git push -u origin main



# 开辟开发分支 触发 pr事件
1）先切到 main 并拉最新
```
git checkout main
git pull origin main
```
这样避免你从一个过期的 main 开分支。

2）创建并切换到新分支

```
git checkout -b feature/review-bot
```
或者

```
git switch -c feature/review-bot
```

3）修改代码后提交

```
git add .
git commit -m "feat: add review report comment logic"
```

4）第一次推送到远端

```
git push -u origin feature/review-bot
```

这里的 -u 很有用，它会建立本地分支和远端分支的跟踪关系。

以后你只需要：

```
git push
```
就行了。

到这里为止，会发生什么？


你刚刚做的是：

```
本地 feature/review-bot -> 远端 origin/feature/review-bot
```
这一步只会触发：

```
on:
  push:
```

还不会触发 pull_request，因为你还没创建 PR。

5）创建 PR（关键步骤）

你需要把：

```
feature/review-bot  ->  main
```
创建成一个 Pull Request。


方法 A：GitHub 网页最简单

你 push 完之后，GitHub 页面通常会直接提示：

Compare & pull request

你点它就行。

然后选择：
	•	base: main
	•	compare: feature/review-bot

然后点击：

Create pull request

方法 B：用 GitHub CLI（更适合你）

如果你装了 GitHub CLI（gh），直接一条命令

```
gh pr create --base main --head feature/review-bot --fill
```

这个命令会：
	•	用当前分支作为 PR 分支
	•	目标分支设为 main
	•	自动用 commit message 填 title/body

如果你想手动写标题和描述

```
gh pr create \
  --base main \
  --head feature/review-bot \
  --title "feat: add review report comment logic" \
  --body "This PR adds PR review comment posting in GitHub Actions."
```

创建 PR 后，什么时候触发 pull_request？

一旦你创建了：

```
feature/review-bot -> main
```

这个 PR，会立刻触发一次：

```
on:
  pull_request:
    branches: [ main ]
```
因为它的 目标分支（base branch） 是 main。

比如你又改了代码：











