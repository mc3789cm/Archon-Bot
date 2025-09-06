from discord import Embed, User

class EmbedManager:
    """
    Manages all Discord embed messages.

    Args:
        primary_color (str): The hexadecimal primary color code for embeds. Default = #1793d1 (Dodger Blue)
        error_color (str): The hexadecimal color code for error embeds. Default = #dc143c (Crimson)
    """
    def __init__(self, primary_color: str = "#1793d1",
                 error_color: str = "#dc143c",
                 bot_name: str = "Bot"):
        self.primary_color = int(primary_color.lstrip("#"), 16)
        self.error_color = int(error_color.lstrip("#"), 16)
        self.bot_name = bot_name

    def join_embed(self) -> Embed:
        return Embed(
            title="Hey!",
            description=f"I'm {self.bot_name}, an all-in-one Discord utility, being only as complex or as simple as you would like me to be. Get started by running `?help`",
            color=self.primary_color,
        )

    def help_embed(self) -> Embed:
        return Embed(
            title="Help Menu",
            description=f"{self.bot_name} is an all-in-one Discord utility, being only as complex or as simple as the admin tailors it to be.",
            color=self.primary_color,
        ).add_field(name="Prefix Commands: (\"?\")",
                    value=f"`?help` - Displays this help message.\n"
                          f"`?ping` - Outputs {self.bot_name}'s websocket and API latencies in milliseconds (`ms`).",
                    inline=False
        ).add_field(name="Slash Commands: (\"/\")",
                    value=f"`/set_admin` - Sets the server *server-wide* admin role.\n"
                          f"This is used to restrict all of the following commands to just the set admin role:\n"
                          f"   - `command_one`\n- `command_two`\n- `command_three`",
                    inline=False)

    def ping_embed(self):
        return Embed(
            title="Pinging...",
            description=None,
            color=self.primary_color,
        )

    def pong_embed(self, ws_latency: int, api_latency: int, sent_by: User) -> Embed:
        return Embed(
            title="Pong",
            description=f"**Websocket Latency:** `{ws_latency}ms`\n"
                        f"**API Latency:** `{api_latency}ms`",
            color=self.primary_color,
        ).set_footer(text=f"Ping issued by: `{sent_by}` ")

    def shutdown_embed(self, sent_by: User) -> Embed:
        return Embed(
            title="Shutting down...",
            description=f"{self.bot_name} is going to shutdown now.",
            color=self.primary_color,
        ).set_footer(text=f"Shutdown issued by: {sent_by}")

    def admin_role_set(self, role: str) -> Embed:
        return Embed(
            title="Admin Role Is Set",
            description=f"The admin role is set to {role}",
            color=self.primary_color,
        )

    def error_forbidden(self) -> Embed:
        return Embed(
            title="Error: Forbidden",
            description="You do not have the required permissions to run this command.",
            color=self.error_color,
        )

    def error_guild_only(self) -> Embed:
        return Embed(
            title="Error: Guild Only",
            description="You can only run this command in a guild (server).",
            color=self.error_color,
        )