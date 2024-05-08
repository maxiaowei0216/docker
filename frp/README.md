# 简介

基于[fatedier/frp](https://github.com/fatedier/frp)的docker镜像，暂仅支持linux/amd64架构。

# Tags
- 0.58.0, 0.58, latest
- 0.57.0, 0.57
- 0.56.0, 0.56
- 0.55.1, 0.55
- 0.54.0, 0.54
- 0.53.2, 0.53
- 0.53.0
- 0.52.3, 0.52

# 使用方法

## docker cli

- 服务端 - frps

```shell
docker run -d \
    --name=frps \
    --network host \
    -e RUN_MODE=server \
    -v /path/to/conf:/frp/conf \
    maxiaowei/frp:latest
```

- 客户端 - frpc

```shell
docker run -d \
    --name=frpc \
    --network host \
    -e RUN_MODE=client \
    -v /path/to/conf:/frp/conf \
    maxiaowei/frp:latest
```

## 参数

| 参数                   | 功能                               |
|:--------------------:| -------------------------------- |
| `-e RUN_MODE=server` | 指定运行模式，server对应frps，client对应frpc |
| `-v /frp/conf`       | 配置文件路径                           |
