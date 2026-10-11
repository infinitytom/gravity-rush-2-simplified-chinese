# 重力眩晕 2 简体中文补丁

为 **Gravity Rush 2 / 重力异想世界完结篇，CUSA04934 亚洲版 1.11** 制作的模拟器文本补丁。

游戏资源包已包含原生简体中文翻译和字体。本补丁将繁体中文资源入口接到这些简体资源上，保留原有文本编号，并补全 9 条繁体表独有的 DLC 文本。**安装后在模拟器中选择“繁体中文”，游戏会加载简体文本。**

> 当前完成的是资源文件校验和安装、恢复验证，尚未在模拟器中实测。欢迎通过 Issues 反馈实际显示效果。图片、贴图或预渲染视频中写死的文字不在本补丁范围内。

## 下载

前往 [Releases](https://github.com/infinitytom/gravity-rush-2-simplified-chinese/releases/latest)，下载附件 **GravityRush2_CUSA04934_SimplifiedChinese_v1.0.zip**。

推荐普通玩家下载 Release 附件。GitHub 自动生成的 “Source code” 压缩包是开发用源码，外层目录结构与补丁附件不同。

发布附件只有补丁脚本、OpenCC 依赖和说明，**不含游戏文件、游戏翻译文本、字体或制作时的备份**。安装时直接从玩家自己的游戏资源中读取所需内容。

## 环境和兼容性

| 项目 | 要求 |
| --- | --- |
| 游戏 | CUSA04934 亚洲版，制作时游戏版本为 1.11 |
| 文件状态 | 已解包、模拟器可直接读取的游戏目录 |
| 必需资源 | `Gravite2_Chunk0.psarc` 和 `Gravite2_Patch_Chunk0.psarc` |
| Python | Python 3.10 或更高版本 |
| Windows 安装入口 | `Install.cmd` 和 `Restore.cmd` |
| 模拟器语言 | 繁体中文 / Chinese (Traditional) |

这不是 PS4 真机可安装的 PKG 文件。其他地区版本、其他更新版本或已经修改过的资源包没有确认兼容。

版本号相同不保证资源完全相同。安装器会比对两个 PSARC 的文件大小和原始索引 SHA-256；不匹配时退出，不修改游戏。兼容指纹见 [supported.json](simplified_patch/supported.json)。

## 安装步骤

### 1. 安装并检查 Python

安装 Python 3.10 或更新版本；使用官方 Windows 安装器时，可勾选 **Add Python to PATH**。安装后重新打开 PowerShell，执行：

```powershell
python --version
```

应显示 `Python 3.10.x` 或更高版本。如果 `python` 不可用，但 `py` 可用，也可以执行：

```powershell
py -3 --version
```

双击安装脚本时会先尝试 `python`，再尝试 `py -3`。OpenCC 已随补丁提供，不需要运行 pip 安装依赖。

### 2. 解压到正确目录

关闭正在运行的游戏。把 Release 附件解压到游戏目录，确保 **simplified_patch 文件夹与 eboot.bin、PSARC 资源包处于同一级**：

```text
CUSA04934/
├─ eboot.bin
├─ Gravite2_Chunk0.psarc
├─ Gravite2_Chunk1.psarc
├─ Gravite2_Patch_Chunk0.psarc
├─ Gravite2_Patch_Chunk1.psarc
├─ sce_sys/
└─ simplified_patch/
   ├─ Install.cmd
   ├─ Restore.cmd
   ├─ install.py
   ├─ restore.py
   ├─ psarc.py
   ├─ supported.json
   ├─ vendor/
   └─ 使用说明.md
```

不要放到 `sce_sys` 中，也不要多套一层压缩包名称文件夹。如果下载的是源码，需要将其中的 `simplified_patch` 文件夹单独复制到上述位置。

### 3. 检查兼容性（可选）

在游戏目录中打开 PowerShell，执行：

```powershell
python simplified_patch/install.py --check
```

使用 Python Launcher 时，将 `python` 替换成 `py -3`。

成功时显示：

```text
Compatibility check passed. No game files were modified.
Replacement resources: 105
```

此命令读取资源并构建替换内容，不会安装补丁或修改游戏文件。

### 4. 安装补丁

双击 `simplified_patch/Install.cmd`。也可以在游戏目录执行：

```powershell
python simplified_patch/install.py
```

安装成功会显示两个资源包的回读验证结果，以及：

```text
Installed successfully. Select Traditional Chinese in your emulator.
```

首次安装会生成 `simplified_patch/backup` 和 `report.json`。**保留 backup 文件夹**，恢复原版需要其中的原始索引和文件长度。每位玩家都应使用自己安装时生成的备份。

### 5. 设置语言并启动

在模拟器的系统语言设置中选择 **繁体中文 / Chinese (Traditional)**；如果存在单独的游戏语言设置，也选择繁体中文。重新启动安装了补丁的这个游戏目录。

这里选择繁体中文，是因为补丁替换了繁体资源入口。设置页面中的语言名称不会改成“简体中文”。具体设置页面位置取决于模拟器及其版本。

## 恢复原版繁体中文

关闭游戏，双击 `simplified_patch/Restore.cmd`，或者在游戏目录执行：

```powershell
python simplified_patch/restore.py
```

恢复脚本先检查补丁后文件长度、资源索引和追加内容，确认一致后写回原始索引并截去追加数据。成功时两个资源包分别显示 `Restored:`。

恢复后可以再次运行 `Install.cmd` 安装。升级游戏、替换 PSARC 或使用其他资源补丁之前，建议先恢复。不要把旧版本的 backup 用于更新后的资源包；若文件已被其他工具修改，恢复脚本会拒绝继续，应先恢复与这份备份匹配的文件。

## 常见问题

### 双击后提示需要 Python，或系统打开 Microsoft Store

先用 `python --version` 或 `py -3 --version` 确认解释器可用。Windows 的应用执行别名可能将 `python` 指向 Microsoft Store；可安装 Python 并配置 PATH，或直接使用 `py -3` 运行脚本。

### 提示 Unsupported or modified game archive / Unsupported archive version

资源包缺失、位置不正确、游戏版本不同，或文件已被修改。检查文件夹层级、CUSA 编号，以及 `supported.json` 中的大小和指纹。请使用匹配的原始资源；不要删除版本检查来强行安装。

### 提示 Patch is already installed

当前补丁文件夹里有有效安装记录。如果游戏显示正常，不需要再次安装。想重新安装，先运行恢复脚本。不要仅删除 backup 来绕过检查。

### 安装成功后仍显示繁体

确认模拟器系统语言为繁体中文，彻底关闭后重新启动游戏，并核对模拟器实际加载的游戏目录。有些环境可能从另一个更新目录加载资源；必须针对实际使用的资源目录安装。

如果只有图片或视频中的文字仍为繁体，这属于本补丁的覆盖限制。

### 出现缺字、乱码、崩溃或部分文本未改变

先用恢复脚本恢复，确认问题是否只在安装补丁后出现。提交 Issue 时请附：游戏 CUSA 编号和版本、模拟器名称和版本、语言设置、出问题的界面或任务、安装输出，以及有问题的截图。请勿上传完整游戏文件或个人备份。

### 提示 PermissionError / 文件正在被使用

关闭游戏和占用资源包的程序，确保当前账号可以写入游戏目录。然后在 PowerShell 中重新运行脚本，以便查看完整错误信息。

### backup 丢失了怎么办

这份补丁依靠本机备份精确恢复，不能使用别人的备份代替。可从自己的未修改副本恢复两个资源包，然后重新安装。

## 补丁如何修改文件

补丁处理 94 个不同的文本表和配套字体配置。由于主包与更新包包含部分相同资源，共修改 105 个资源条目：主包 92 个、更新包 13 个。

- 按文本编号使用游戏自带的 CS 简体中文记录，保留 CT 繁体表原有的编号集合。
- 9 条缺少对应简体记录的 DLC 文本使用 OpenCC `t2s` 转换，并保留原有长度和排版数据。
- 繁体字体表使用游戏原生简体字体配置。
- 新资源追加到 PSARC 尾部，只更新相关索引和压缩块长度，原始资源数据保持在原位。
- 主包追加 629098 字节，更新包追加 162153 字节，总共 791251 字节，约 773 KiB。
- 不修改 `eboot.bin`、其他 PSARC、存档或模拟器设置。

备份保存原始索引和文件长度，无需另复制整个约 10 GB 主包。`report.json` 记录各个替换资源的路径、文本数量和 SHA-256。

## 已完成的验证

- 两个修改后的 PSARC 均可由读取器解析。
- 所有 105 个替换条目解压后与生成内容逐字节一致。
- 文本编号及内部偏移可解析，原有编号没有丢失。
- 未修改条目的索引和压缩块长度保持一致。
- 原版恢复、兼容性检查和重新安装均已执行并通过。
- 发布 ZIP 完整性检查通过，排除游戏资源、个人备份、检查时导出的文件和 Python 缓存。

以上为文件层面的验证，不能替代游戏实测。

## 源码、依赖与许可

源码位于 [simplified_patch](simplified_patch)。本项目补丁脚本使用 [MIT License](LICENSE)。随附 OpenCC Python 实现 0.1.7 使用 Apache-2.0，见 [第三方说明](THIRD_PARTY_NOTICES.md) 及 vendor 中保留的许可。游戏内容不属于本项目许可范围。

如需修改并分享补丁，请保留版本检查、恢复机制及第三方许可，并明确说明自己的改动与验证情况。
