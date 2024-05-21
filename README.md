# GitHub Star README DOWNLOAD

包含了三种不同下载方法，任选其一即可。

## 1 一次性下载

配置环境变量，然后运行 main.py 即可

```
export GITHUB_USERNAME=<你的 GitHub 用户名>
export GITHUB_TOKEN=<你的 GitHub 访问令牌>
```

---

## 2 后台监控 API 更新

### 配置环境变量
```
export GITHUB_USERNAME=<你的 GitHub 用户名>
export GITHUB_TOKEN=<你的 GitHub 访问令牌>
export BASE_DIR=<README 文件存储的根目录>
```

### 后台运行脚本

（比如说在 .zshrc 中添加）

```
if ! pgrep -f 'update.py' > /dev/null; then
    nohup python3 /path/to/update.py > /path/to/logfile.log 2>&1 &
fi
```

---

## 3 监控 RSS 订阅源

### 配置环境变量
```
export BASE_DIR=<README文件存储的根目录>
export FEED_URL=<RSS订阅源URL>
```

### 后台运行脚本

```bash
if ! pgrep -f 'monitor_rss.py' > /dev/null; then
    nohup python3 /path/to/monitor_rss.py > /path/to/logfile.log 2>&1 &
fi
```