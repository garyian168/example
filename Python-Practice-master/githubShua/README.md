Python Script之指定github Commit日期
===

### 前期准备

使用平台: Linux

1.将你的Linux root用户公钥传到github Setting

2.创建一个名为Test的空仓库

### 如何使用？

1.修改config.py里相应的值：

- `dest_date`: 你想指定的git commit日期，格式为"2014/12/12"
- `github_name`: 你的github名
- `github_email`: 你的github邮箱

2.`sudo python bootStrap.py`

3.然后你会发现你github用户首页相应日期的灰色格子变成绿色，完成了那天的commit

### 备注

git commit依据的时间是本地git仓库时间(即ubuntu操作系统时间)，运行完脚本需要将你ubuntu时间再改回来

脚本很简单，本着娱乐的目的写的这个脚本