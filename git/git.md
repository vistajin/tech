https://nvie.com/posts/a-successful-git-branching-model/

#### 恢复某个文件到某个版本

```
git log

commit 7894c8479abfc79229c23fe7e40d3f49591ed9c7
Author: vistajin <528189@qq.com>
Date:   Sat Jul 4 00:38:26 2020 +0800

    minor update for sed

commit e9e5f45982a0490cf7193b8103211d2f3012dee6
Author: vistajin <528189@qq.com>
Date:   Thu Jul 2 23:55:39 2020 +0800

    add vi.md

git checkout e9e5f45982a0490cf7193b8103211d2f3012dee6 vi.md
```

