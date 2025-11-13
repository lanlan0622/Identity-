import re
import requests
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
from astrbot.core.message.components import BaseMessageComponent

@register(
    "astrbot_plugin_github_auth",
    "lanlan0622",
    "GitHub身份认证插件，支持QQ绑定GitHub账号",
    "1.0.0",
    "https://github.com/lanlan0622/Identity-.git"
)
class GitHubAuthPlugin(Star):
    def __init__(self, context: Context, config):
        self.config = config
        self.auth_pattern = re.compile(r"^(!|\/)github-auth\s+(\S+)$", re.IGNORECASE)
        self.admin_qq = 2869707290  # 改这里：去掉引号，用整数类型
        super().__init__(context)

    @filter.on_decorating_result()
    async def handle_auth(self, event: AstrMessageEvent):
        result = event.get_result()
        msg_chain = result.chain
        new_chain = []
        current_user_qq = event.user_id  # 改这里：不用转字符串，保持整数

        msg_text = ""
        for comp in msg_chain:
            if comp.type == "Plain":
                msg_text += comp.text
            new_chain.append(comp)

        match = self.auth_pattern.match(msg_text.strip())
        if not match:
            result.chain = new_chain
            return

        username = match.group(2)
        if not self._check_github_user(username):
            new_chain.append(Comp.Plain(text=f"\n❌ GitHub用户「{username}」不存在"))
            result.chain = new_chain
            return

        reply = (
            f"\n✅ 认证请求已提交\n"
            f"QQ：{current_user_qq}\n"
            f"GitHub：{username}\n"
            f"@管理员({self.admin_qq}) 请审核"
        )
        new_chain.append(Comp.Plain(text=reply))
        if not event.is_private_chat():
            new_chain.append(Comp.At(qq=self.admin_qq))  # 这里现在是整数，匹配要求

        result.chain = new_chain

    def _check_github_user(self, username: str) -> bool:
        try:
            resp = requests.get(
                f"https://api.github.com/users/{username}",
                timeout=5,
                headers={"User-Agent": "AstrBot-Plugin"}
            )
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"GitHub验证失败: {e}")
            return False
