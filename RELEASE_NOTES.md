# v1.0.0：重力眩晕 2 简体中文补丁

启用 CUSA04934 亚洲版 1.11 资源包中的原生简体中文文本与字体，覆盖 94 个文本表，并补全 9 条繁体表独有的 DLC 文本。

## 下载与安装

1. 下载下方附件 `GravityRush2_CUSA04934_SimplifiedChinese_v1.0.zip`，无需下载完整源码。
2. 安装 Python 3.10 或以上版本。
3. 关闭游戏，把 ZIP 解压到游戏目录，使 `simplified_patch` 与 `eboot.bin` 处于同一级。
4. 双击 `simplified_patch/Install.cmd`；看到 `Installed successfully` 后，将模拟器语言设为 **繁体中文 / Chinese (Traditional)** 并启动游戏。
5. 保留安装时生成的 `simplified_patch/backup`。需要恢复时，关闭游戏后双击 `Restore.cmd`。

完整教程、目录示例、命令行操作及故障排查见 [README](https://github.com/infinitytom/gravity-rush-2-simplified-chinese#readme)。

## 适用范围与验证

仅适用于资源指纹匹配的 CUSA04934 亚洲版 1.11 已解包目录；安装前自动检查两个 PSARC 的大小和索引 SHA-256。不是 PS4 真机 PKG。

补丁包不含游戏文件、翻译文本、字体或个人备份。原生简体资源从玩家自己的游戏文件读取，OpenCC 依赖已附带，无需另装依赖。

105 个修改资源条目均完成解压回读比对，并通过恢复、兼容性检查和重装验证。**尚未进模拟器实测**；图片和预渲染视频中的繁体文字不在此次覆盖范围内。

附件另提供 SHA-256 校验文件。
