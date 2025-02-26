# 夸克网盘自动签到

本项目实现了夸克网盘的自动签到功能，通过 GitHub Actions 自动执行，领取每日签到奖励空间，让用户无需手动签到。
本项目基于 `BNDou`大佬的项目中夸克网盘自动签到的子功能 https://github.com/BNDou/Auto_Check_In 修改而来

## 功能简介

- **每日自动签到**：定时运行脚本完成每日签到，领取成长奖励。
- **GitHub Actions 托管**：代码托管在 GitHub 上，设置后每天定时自动执行，实现真正的“一劳永逸”。

## 使用指南

### 1. Fork 项目

点击右上角的 `Fork` 按钮，将本项目复制到自己的 GitHub 仓库。

### 2. 配置 Cookie 信息

项目通过 GitHub Secrets 来配置用户的 Cookie 信息。具体步骤如下：

1. **获取 COOKIE_QUARK**

   【手机端】必须使用手机端抓包，小白推荐使用[proxypin](https://github.com/wanghongenpin/proxypin)或[Reqable]，需要开启root权限才能抓到包
   
- 打开抓包工具，手机端访问签到页，

- 找到url为 https://drive-m.quark.cn/1/clouddrive/capacity/growth/info 的请求信息

- 复制url后面的参数: kps sign vcode 粘贴到环境变量

- 环境变量名为 COOKIE_QUARK 多账户用 回车 或 && 分开，例如:（可以直接把你填入的值中的 & 符号替换成 英文分号，不然很容易配错cookie值）

- `user=张三; kps=abcdefg; sign=hijklmn; vcode=111111111;`
> user字段是用户名 (可是随意填写，多账户方便区分)

2. **添加到 GitHub Secrets**
   - 打开你的 Fork 仓库，进入 **Settings -> Secrets and variables -> Actions**。
   - 点击 **New repository secret** 按钮，创建一个名为 `COOKIE_QUARK` 的 Secret。
   - 将刚才配置好的 Cookie 粘贴到值中，保存。
   
### 3. 配置推送

   目前支持钉钉群机器人推送和微信的WxPusher推送，如果你不需要推送，可以跳过直接继续下一步

1. **钉钉群机器人推送配置**
- 打开`钉钉电脑客户端/要接收消息的钉钉群/群设置（右上齿轮）/机器人/添加机器人/自定义`，配置机器人名字，安全设置选择`自定义关键词`（只有包含关键词的消息才会被推送），输入你要的词，如`夸克`
- 复制机器人的 `Webhook地址` 备用
- 跟配置 `COOKIE_QUARK` 一样，在`GitHub Secrets`下配置创建一个名为 `DINGTALK_WEBHOOK` 的 Secret
- 将上面复制的 `Webhook地址` 粘贴进去保存

2. **WxPusher微信消息推送配置**
- 打开WxPusher官网(https://wxpusher.zjiecode.com/admin/main)，微信扫码登录, 会要求让你创建应用
- 创建好应用，复制 `AppToken` 备用
- `应用管理/应用信息` 扫码关注你创建好的应用，然后在 `用户管理/用户列表` 里找到新增的用户信息，复制 `UID` 备用
- 跟配置 `COOKIE_QUARK` 一样，在`GitHub Secrets`下配置分别创建一个名为 `WX_PUSHER_APP_TOKEN` 的 Secret 和一个 名为 `WX_PUSHER_UID` 的 Secret ，将上面复制的 `AppToken` 和 `UID` 分别粘贴进去保存

### 4. 配置定时任务(Cron Job)时间

1. 修改时间
- 建议修改，和别人的签到时间错开，避免检测，如果要修改自动运行时间，修改的文件的路径 `.github/workflows/quark_signin.yml`，修改cron后面的参数，修改前2个参数就行，第一个表示分钟，第二个表示小时，时间是UTC时间，即北京时间减去8小时，如要配置早上10：45自动运行，就改成 `45 2 * * *`

2. 参数格式
- 符号 `*` 表示通配数值，即匹配任意数值，如配 `30 * * * *` 表示在每天每小时的30分运行
- 符号 `,` 表示多值分隔，如配 `15,45 * * * *` 表示在每天每小时的15分和45分运行
- 符号 `-` 表示数值范围，如配 `30 10-13 * * *` 表示在每天的10、11、12、13点的30分运行
- 符号 `/` 表示步进间隔，如配 `20/15 10 * * *` 表示在每天的10点20分开始到10点59分为止，每隔15分钟运行(10点20分、10点35分、10点50分)

当然我们每天只需要运行一次，使用第一个符号 `*` 就够了

### 5. 启用 GitHub Actions

1. 在你的仓库中，进入 **Actions** 选项卡。
2. 启用 GitHub Actions，会看到 `Quark Sign-in` 工作流已配置完成。
3. 系统会每天自动执行签到脚本，并输出签到结果。

### 6. 手动测试运行

如果想立即测试签到脚本是否配置成功，可以手动触发执行：

1. 进入 **Actions** 选项卡，点击 `Quark Sign-in`。
2. 点击右侧的 **Run workflow**，手动触发一次签到任务，检查是否成功运行。

### 常见问题

- **签到失败或错误提示**：确认 Cookie 信息准确无误，且格式正确（`user=xxx; kps=xxx; sign=xxx;`）。
- **GitHub Actions 配置未生效**：确认 Fork 项目后，启用 GitHub Actions。

### 注意事项

- 本项目仅用于学习用途，请勿用于非法用途。
- 夸克网盘可能会更新接口或规则，导致签到脚本失效，届时需要重新获取 Cookie 并更新代码。

## 免责声明

本项目为开源学习项目，作者不对项目使用产生的后果负责。使用过程中如有疑问，请参考夸克网盘的官方使用条款。

---

此项目由 GitHub Actions 托管，开放源码，欢迎提交 PR 一起优化！
