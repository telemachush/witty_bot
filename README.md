# 🤖 Witty Bot - Slack Status Generator

A fun and intelligent Slack bot that generates witty, professional status messages for your Slack workspace. Perfect for adding some humor to your daily status updates!

## ✨ Features

- **Funny Status Messages**: Generate humorous but professional status messages
- **Multiple Status Types**: Support for busy, away, lunch, break, meeting, and more
- **Slack Integration**: Works seamlessly with Slack slash commands
- **Template-Based**: Uses pre-written funny templates for instant responses
- **Professional**: Filters out inappropriate content
- **Easy Deployment**: One-click deployment to Railway, Render, or other platforms

## 🚀 Quick Start

### Option 1: Deploy to Railway (Recommended)

1. **Fork this repository** to your GitHub account
2. **Sign up** at [railway.app](https://railway.app)
3. **Connect your GitHub** repository
4. **Deploy**: Railway will automatically detect the Dockerfile and deploy
5. **Set environment variables** in Railway dashboard:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   SLACK_SIGNING_SECRET=your-signing-secret-here
   LLM_PROVIDER=templates
   ```
6. **Get your URL**: Railway provides a URL like `https://your-app.railway.app`
7. **Configure Slack**: Set Request URL to `https://your-app.railway.app/slack/events`

### Option 2: Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/witty_bot.git
   cd witty_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your Slack credentials
   ```

4. **Run locally**:
   ```bash
   python app_http.py
   ```

5. **Use ngrok for testing**:
   ```bash
   ngrok http 5000
   ```

## 📋 Slack App Setup

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Give it a name (e.g., "Witty Bot") and select your workspace

### 2. Configure OAuth & Permissions

Add these **Bot Token Scopes**:
- `chat:write` - Send messages
- `commands` - Respond to slash commands
- `im:write` - Send direct messages

### 3. Create Slash Command

1. Go to "Slash Commands" in the left sidebar
2. Click "Create New Command"
3. Configure:
   - **Command**: `/witty_status`
   - **Request URL**: `https://your-app-url.com/slack/events`
   - **Short Description**: `Generate funny status messages`
   - **Usage Hint**: `[busy|away|lunch|break|etc]`

### 4. Install App

1. Go to "OAuth & Permissions"
2. Click "Install to Workspace"
3. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

## 🎯 Usage

### Available Commands

- `/witty_status busy` - Generate a busy status
- `/witty_status away` - Generate an away status
- `/witty_status lunch` - Generate a lunch status
- `/witty_status break` - Generate a break status
- `/witty_status meeting` - Generate a meeting status
- `/witty_status focus` - Generate a focus status
- `/witty_status` - Show help and available options

### Status Types

| Type | Description | Example |
|------|-------------|---------|
| `busy` | Working on something important | "Drowning in code and loving it" |
| `away` | Not available | "Probably getting coffee" |
| `lunch` | Eating lunch/dinner | "Eating my feelings" |
| `break` | Taking a break | "Taking a mental health break" |
| `meeting` | In a meeting | "In a meeting that could have been an email" |
| `focus` | Deep work mode | "Do not disturb (seriously)" |

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SLACK_BOT_TOKEN` | Your Slack bot token | ✅ | - |
| `SLACK_SIGNING_SECRET` | Your Slack app signing secret | ✅ | - |
| `LLM_PROVIDER` | LLM provider (openai, ollama) | ❌ | `openai` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) | ❌ | - |
| `OLLAMA_MODEL` | Ollama model name | ❌ | `tinyllama:1b` |

### LLM Providers

1. **OpenAI** (Recommended): Uses GPT-3.5-turbo for dynamic responses
2. **Ollama**: Uses local LLM models (requires more resources)

## 🐳 Docker Deployment

The app is containerized and ready for deployment:

```bash
# Build the image
docker build -t witty-bot .

# Run locally
docker run -p 5000:5000 \
  -e SLACK_BOT_TOKEN=your-token \
  -e SLACK_SIGNING_SECRET=your-secret \
  -e LLM_PROVIDER=templates \
  witty-bot
```

## 📁 Project Structure

```
witty_bot/
├── app_http.py          # Main Flask application
├── app.py               # Legacy Slack app (not used)
├── config.py            # Configuration and templates
├── llm_client.py        # LLM client for different providers
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── env.example          # Environment variables template
├── railway.json         # Railway deployment config
└── README.md           # This file
```

## 🔧 Development

### Adding New Status Types

1. **Add to `config.py`**:
   ```python
   STATUS_TYPES = {
       "your_type": "Description of the status type",
       # ... existing types
   }
   ```

2. **Add templates**:
   ```python
   STATUS_TEMPLATES = {
       "your_type": [
           "Funny message 1",
           "Funny message 2",
           # ... more messages
       ],
       # ... existing templates
   }
   ```

### Adding New LLM Providers

1. **Add provider initialization** in `llm_client.py`
2. **Add generation method** for the new provider
3. **Update configuration** in `config.py`

## 🚨 Troubleshooting

### Common Issues

1. **"URL verification failed"**
   - Ensure your URL is publicly accessible
   - Check that the endpoint returns 200 OK
   - Verify SSL certificate (https://)

2. **"Command not found"**
   - Check that the slash command is properly configured
   - Verify the app is installed to your workspace
   - Check bot token permissions

3. **"not_in_channel" error**
   - The bot sends direct messages by default
   - No need to add the bot to channels

4. **Ollama memory issues**
   - Use `LLM_PROVIDER=templates` for reliable operation
   - Or use smaller models like `tinyllama:1b`

### Environment Variables Checklist

```bash
# Required
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# Optional (recommended for Railway)
LLM_PROVIDER=templates
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Slack Bolt](https://slack.dev/bolt-python/)
- Deployed on [Railway](https://railway.app)
- Inspired by the need for more humor in professional communication

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [Slack API documentation](https://api.slack.com/)
3. Open an issue on GitHub

---

**Happy status generating! 🎉**
