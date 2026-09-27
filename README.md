<p align="center">
  <img src="assets/cockpit-logo.png" width="280" alt="cockpit 驾驶舱" />
</p>

<p align="center"><strong>cockpit 驾驶舱 · AI 开发实作</strong></p>
<h1 align="center">把业务需求，做成看得见、用得上的系统。</h1>
<p align="center">从需求拆解到系统实现，记录 AI 开发的真实过程。</p>
<h2 align="center">固定资产盘点看板</h2>
<p align="center">喜文FDE案例系列</p>
<p align="center">资产管理 · 资产登记、实盘数量与差异追踪 · 业务演示系统</p>
<p align="center"><a href="https://resume.fangnan.club/cockpit/">了解 cockpit</a> · <a href="https://resume.fangnan.club/">认识作者</a></p>


## 认识作者，一起把想法做出来

**我是方楠，智能体工程师 / 全栈工程师。**

专注 AI 编程、智能体开发与业务系统落地，具备 Python、前后端开发、数据工程与技术交付经验。从需求梳理、架构设计到系统实现，关注技术怎样解决具体业务问题。

这里分享我使用 cockpit 驾驶舱开展 AI 开发的项目：需求怎样拆、系统怎样做、业务流程怎样验证。希望这些可查看、可复现的实现，为你的下一个项目提供参考。

**有相似需求？欢迎交流业务场景、AI 开发实践与项目合作。**

| 了解我 / 联系我 | 入口 |
| :--- | :--- |
| 个人主页 | [方楠 · 个人简历](https://resume.fangnan.club/) |
| 电话 / 微信 | 16607557430 |
| 合作邮箱 | [16607557430@163.com](mailto:16607557430@163.com) |
| 抖音 | 智效上门AI解决方案 · 抖音号：74759905847 |
| cockpit 介绍 | [了解 cockpit 驾驶舱](https://resume.fangnan.club/cockpit/) |

<p align="center">
  <img src="assets/douyin-qr-placeholder.svg" width="200" alt="抖音二维码待提供；此处为不可扫码的版式占位" />
</p>
<p align="center"><strong>关注我的抖音，看需求如何一步步变成系统。</strong><br />真实开发过程 · 系统操作演示 · 项目复盘</p>

作者介绍与联系方式整理自[个人简历网站](https://resume.fangnan.club/)。抖音二维码原图待补。

<p align="center"><strong>喜欢这类项目，欢迎 Star 收藏，也欢迎通过 Issues 一起完善。</strong></p>

---

## 固定资产盘点看板解决什么问题？

面向资产管理，围绕“资产登记、实盘数量与差异追踪”提供可操作的演示系统。当前交付状态：**已完成中台功能验收**。

## 系统架构

```text
浏览器页面 → JavaScript 校验与业务计算 → localStorage
浏览器页面 ← 列表 / 指标 / CSV ← 当前浏览器中的演示记录
```

cockpit 用于 AI 开发过程，不是此系统运行的必需服务。本系统没有因为使用 AI 开发而自动接入运行时大模型。

## 本地运行

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 http://127.0.0.1:8000/index.html 。无需构建或后端依赖，也可直接打开 index.html；建议固定 HTTP 地址，避免浏览器存储来源变化。

## 代码目录

```text
index.html     页面、样式与业务逻辑
smoke-test.py  独立浏览器功能测试
assets/       README 品牌素材
README.md      项目说明
LICENSE        MIT 许可证
```

## 操作与业务规则


入口：当前目录 `index.html`，单文件内嵌 CSS / JavaScript，无外部 CDN 或网络接口。身份标识为 douyin。

## 本地访问


如需宿主机本地 HTTP 预览，在当前项目目录运行：

```bash
python3 -m http.server 8011 --bind 127.0.0.1
```

对应地址为 `http://127.0.0.1:8011/index.html`（需启动服务；只对宿主机本地开放）。不同协议、主机或端口的浏览器存储彼此独立。

## 操作验收

1. 点击“登记资产”，输入虚构编号 `XN-9001`、名称“演示测试设备”、楼层“三楼”、台账数量 `10`，保存。
2. 在“扫码盘点”输入 `XN-9001`，查找后实盘数量输入 `7`，保存。
3. 该资产盘亏 `3`；全量台账 `120`、实盘 `90`、差异 `3` 条；三楼台账 `32`、实盘 `17`。
4. 刷新页面，新增资产与盘点数据保持不变。
5. 使用“修改”更改台账数量或楼层，差异及楼层分布自动更新；筛选影响列表和 CSV 导出，顶部指标始终统计全部资产。
6. 重置必须二次确认；取消保留现有数据。CSV 是导出留存，不支持导入恢复。

盘点输入的是该编号的实盘总数量，重复登记覆盖上次结果；未盘点不计入盘亏。编号代表一条资产台账，可有多台同类设备。楼层依据台账登记位置，不采集实物楼层差异。

## 可重复测试

在宿主机、同路径挂载的当前项目目录执行：

```bash
python3 smoke-test.py
```

依赖宿主机 Python Playwright 和其 Chromium 浏览器。脚本开启临时回环 HTTP 服务，使用隔离浏览器上下文，不改用户浏览器数据；结束关闭服务。生成 `development-result.json`、`evidence-desktop.png` 和 `evidence-mobile.png`。

实际结果：23 项浏览器功能检查通过；包含新增、模拟扫码、差异/楼层联动、刷新、修改、组合筛选、CSV、错误输入、零实盘、确认重置、分页、手机布局、损坏存储处理及脚本异常检查。未进行几万条资产的性能压测。

## 能力边界与待补

- 演示数据·仅当前浏览器保存，键为 `development-11-assets-v1`；无真实后台、多用户同步或身份认证。
- 扫码是虚构编号输入模拟，无摄像头或硬件接入。只填写脱敏演示信息。
- 数据保存失败时会明确提示；损坏存储不静默覆盖，需用户确认重置。

## 验证范围

发布前在独立导出目录验证启动与入口访问；实际结果随发布回执记录。业务验收状态与代码发布状态分开管理。原有测试记录属于历史开发验证，不代表生产环境验收。

## 交流与贡献

使用问题请在本仓库 Issues 提供环境、复现步骤与脱敏截图。欢迎提交改进建议或 Pull Request；业务交流见顶部公开联系方式。如果对你有帮助，欢迎 Star 收藏。

## 项目地址

- GitHub: https://github.com/fn199544123/cockpit-fde-11-asset-inventory
- 码云: https://gitee.com/xiwenfde/cockpit-fde-11-asset-inventory.git

## 许可证

本项目原创代码采用 [MIT](LICENSE)，允许在遵守许可声明的前提下使用、修改与商用。第三方组件适用各自许可证；cockpit 品牌素材用于项目归属展示，不代表商标授权或官方背书。

演示数据均为虚构编号与通用业务信息，不代表真实客户经营数据。

---

<p align="center"><strong>cockpit 驾驶舱 · 喜文FDE案例系列</strong></p>
