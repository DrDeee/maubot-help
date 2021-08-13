# maubot-help
A simple help plugin for [MauBot](https://github.com/maubot/maubot), which allows you to store the help messages
centrally as a JSON file.

## Usage
### Setup
1. Install the plugin with the GUI of Maubot
2. Add your Matrix ID to the developers
3. Create a category index and a command index (see [here](https://github.com/drdeee/matrix-help-index))
4. Execute `!help reload`

### Commands
`!help`: Shows all commands
`!help <command name>`: Shows infos for a specified command
`!help reload`: Reload the indexes, only for developers
