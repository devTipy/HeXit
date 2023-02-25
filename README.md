# Discord HeXit Mathematics Bot

This is a bot for [Discord](https://discordapp.com/) that automatically renders LaTeX & TeX formulas.

## Invocation

By default, the bot can be invoked with `!tex [LaTeX Code]`. Using `!help` or `!help tex` will private message the help.

Example: `!tex \sqrt{a^2 + b^2} = c`

### Channels

The list of servers and channels that the bot may access. The rules are as follows:

1. If the whitelist is empty, the bot may access all channels on all servers.
2. If the whitelist is not empty, the bot may access only the *servers* on the whitelist.
3. The bot may not access any *server* on the blacklist.
4. The bot may access any *channel* on the whitelist.
5. The bot may not access any *channel* on the blacklist.

Rules with larger numbers overrule the smaller ones.

### Renderer

`remote` will use an external server to render the LaTeX. **I do not own or maintain this server.**
Consider finding a different server. If too many people abuse it, it will be shut down.

`local` will attempt to use the programs `latex` and `dvipng` to render the LaTeX locally.