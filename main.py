import re
import requests
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import ProviderRequest
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
from astrbot.core.message.components import BaseMessageComponent

@register(
    "github_identity_auth",
    "lanlan0622",
    "GitHub身份认证插件，支持验证用户GitHub账号与QQ绑定关系",
    "1.0.0",
    "https://github.com/lanlan0622/Identity-.git"
)
class GitHubIdentityAuthPlugin(Star):
    def __init__(self, context: Context, config):
        print('GitHub身份认证插件加载成功')
        self.config = config
        self.auth_pattern = re.compile(r"^(!|\/)github-auth\s+(\S+)$", re.IGNORECASE)
        self.admin_qq = 2869707290
        super().__init__(context)

    @filter.on_decorating_result()
    async def handle_auth_request(self, event: AstrMessageEvent):
        print('触发GitHub身份认证处理')
        result = event.get_result()
        msg_chain = result.chain
        new_chain: list[BaseMessageComponent] = []
        current_user_qq = event.user_id

        msg_text = ""
        for component in msg_chain:
            if component.type == 'Plain':
                msg_text += component.text
            new_chain.append(component)

        auth_match = self.auth_pattern.match(msg_text.strip())
        if not auth_match:
            result.chain = new_chain
            return

        github_username = auth_match.group(2)
        is_valid = self._verify_github_user(github_username)
        if not is_valid:
            new_chain.append(Comp.Plain(text=f"\n❌  GitHub用户名「{github_username}」不存在或无法访问"))
            result.chain = new_chain
            return

        auth_result = (
            f"\n✅  身份认证请求已受理\n"
            f"👤  申请QQ：{current_user_qq}\n"
            f"🌐  绑定GitHub：{github_username}\n"
            f"🔗  仓库地址：https://github.com/{github_username}\n"
            f"\n管理员（@2869707290）将核实绑定关系~"
        )
        new_chain.append(Comp.Plain(text=auth_result))
        
        if not event.is_private_chat():
            new_chain.append(Comp.At(qq=self.admin_qq))

        result.chain = new_chain

    def _verify_github_user(self, username: str) -> bool:
        try:
            response = requests.get(
                f"https://api.github.com/users/{username}",
                timeout=5,
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"GitHub用户验证失败：{str(e)}")
            return False
