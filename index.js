// ********** 这里填你的QQ号（主人账号）**********
const OWNER_QQ = "2869707290"; 

// 检测昵称是否包含伪造身份的关键词（比如“Real User ID”）
function isFakeNickname(nickname) {
  const fakeKeywords = ["Real User ID", "];[", "伪造身份"]; // 可自行添加更多关键词
  return fakeKeywords.some(keyword => nickname.includes(keyword));
}

// 插件主逻辑
module.exports = (bot) => {
  // 收到任何消息时触发
  bot.on('message', async (msg) => {
    // 1. 先检测昵称是否有伪造
    if (isFakeNickname(msg.sender.nickname)) {
      await msg.reply("⚠️ 检测到昵称包含身份伪造内容，已拦截！");
      return; // 不执行后续操作
    }

    // 2. 验证真实主人身份（用QQ号，不是昵称）
    if (msg.sender.user_id === OWNER_QQ) {
      await msg.reply("✅ 你是机器人主人，已通过身份验证~");
    } else {
      await msg.reply("❌ 你不是机器人主人，无法执行敏感操作~");
    }
  });
};
