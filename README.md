# Astrbot身份认证插件

让bot支持GitHub账号与QQ的绑定认证，需配合管理员审核使用

## 功能说明
- 群聊/私聊发送指令即可发起认证
- 自动验证GitHub用户名有效性
- 群聊中自动@管理员提醒审核
- 展示用户QQ、GitHub账号及仓库链接

## 使用方法
1. 在聊天框发送认证指令（两种格式均可）：
   - `!github-auth 你的GitHub用户名`
   - `/github-auth 你的GitHub用户名`

2. 示例：
  !github-auth lanlan0622
 3. 效果：
- 插件自动验证用户名是否存在
- 返回认证受理通知，群聊中@管理员（QQ：2869707290）
- 管理员核实后完成绑定关系确认

## 依赖说明
- 插件需要网络权限（调用GitHub公开API）
- 无需额外配置，直接加载即可使用
- 管理员QQ已内置为：2869707290（可在main.py中修改）

## 仓库地址
https://github.com/lanlan0622/Identity-.git
