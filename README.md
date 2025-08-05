# Clash of Clans Clan Member Inviter

An automated tool for inviting players to your Clash of Clans clan based on customizable filters.

## What This Does

This tool automatically:
- Searches for potential clan members in Clash of Clans
- Filters players by town hall level, trophy count, and troop levels
- Sends invitations to players who meet your criteria
- Uses the official Clash of Clans API to get player information

## Quick Start

```bash
# Setup the project (creates virtual environment and installs dependencies)
make setup

# Run the main script
make run

# Or do everything in one command
make quick-start
```

## Prerequisites

- **BlueStacks 5** running Clash of Clans in full-screen mode (1920x1080 resolution)
- **Clash of Clans API Token** - Get one from [Clash API Developer Portal](https://developer.clashofclans.com/#/login)

## Setup

1. **Get your API token** from the Clash of Clans developer portal
2. **Set up your API token securely** (choose one method):
   
   **Option A: Environment Variable**
   ```bash
   export CLASH_API_TOKEN='your_clash_api_token_here'
   ```
   
   **Option B: .env file**
   ```bash
   cp env.example .env
   # Edit .env and add your token
   ```
   
3. **Run the setup**:
   ```bash
   make setup
   ```

## Usage

1. **Start BlueStacks 5** and open Clash of Clans
2. **Run the script**:
   ```bash
   make run
   ```
3. **Enter the number** of players you want to invite
4. **Click into the BlueStacks window** to focus it
5. **Let the automation run** - it will search and invite players automatically

## Configuration

### Screen Coordinates
The tool uses specific screen coordinates for clicking buttons. If you have a different screen resolution, you may need to adjust these in `src/clash.py`:

```python
self.positions = {
    'game_area': (1373, 35),
    'my_clan': (809, 66),
    'find_new_members': (516, 733),
    # ... more positions
}
```

### Player Filters
You can customize the filtering criteria in the code. Currently it filters for:
- Town Hall 9+ players
- 1000+ trophies
- Level 4+ archers and barbarians

## Available Commands

```bash
# Show all available commands
make help

# Environment Management
make venv              # Create Python virtual environment
make venv-activate     # Show how to activate environment
make venv-deactivate   # Show how to deactivate environment

# Dependencies
make install           # Install project dependencies
make setup             # Create venv and install dependencies

# Running the Project
make run               # Run the main clash.py script
make test              # Run the tester.py script

# Maintenance
make clean             # Remove virtual environment and cache files
make dev               # Development mode with auto-restart

# Quick activation
./activate.sh          # Activate environment and start interactive shell
```

## How It Works

1. **Screen Automation**: Uses `pyautogui` to click buttons and navigate the Clash of Clans interface
2. **API Integration**: Fetches player data from the official Clash of Clans API
3. **Smart Filtering**: Evaluates players based on your criteria before sending invitations
4. **Automated Inviting**: Sends invitations to qualified players automatically

## Troubleshooting

- **Wrong screen coordinates**: Adjust the position values in the code for your screen resolution
- **API token issues**: Make sure your token is valid and has the necessary permissions
- **BlueStacks not responding**: Ensure BlueStacks is in focus and running at 1920x1080 resolution

## Dependencies

- Python 3.x
- BlueStacks 5
- Clash of Clans API token
- Various Python packages (automatically installed via `make setup`)

## License

This project is for educational purposes. Please respect Clash of Clans' terms of service when using this tool.
