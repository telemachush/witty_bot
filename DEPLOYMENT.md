# Deployment Guide for StatusSage Bot

This guide covers multiple deployment options for your Slack Status Bot with Docker containerization.

## 🐳 Docker Containerization

The app is now fully containerized with Ollama included, making it easy to deploy anywhere!

## 🚀 Quick Deploy Options

### Option 1: Railway with Docker (Recommended - Easiest)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub** repository
3. **Deploy**: Railway will automatically detect the Dockerfile and deploy
4. **Set environment variables** in Railway dashboard:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `LLM_PROVIDER=ollama` (recommended for containerized deployment)

5. **Get your URL**: Railway provides a URL like `https://your-app.railway.app`

6. **Configure Slack**:
   - Go to your Slack app settings
   - Set Request URL to: `https://your-app.railway.app/slack/events`

**Note**: The Docker container includes Ollama and will automatically download the Llama 2 model on first startup.

### Option 2: Render with Docker (Free Tier Available)

1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub** repository
4. **Configure**:
   - Build Command: `docker build -t status-bot .`
   - Start Command: `docker run -p 5000:5000 status-bot`
   - Environment: Docker

5. **Set environment variables** in Render dashboard:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `LLM_PROVIDER=ollama`

6. **Deploy** and get your URL
7. **Configure Slack** with the URL + `/slack/events`

### Option 3: Heroku (Paid)

1. **Install Heroku CLI**
2. **Deploy**:
   ```bash
   heroku create your-status-bot
   git push heroku main
   heroku config:set SLACK_BOT_TOKEN=your-token
   heroku config:set SLACK_SIGNING_SECRET=your-secret
   heroku config:set LLM_PROVIDER=openai
   heroku config:set OPENAI_API_KEY=your-key
   ```

3. **Configure Slack** with: `https://your-app.herokuapp.com/slack/events`

### Option 4: DigitalOcean App Platform

1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create App** from GitHub repository
3. **Configure** environment variables
4. **Deploy** and get your URL
5. **Configure Slack** with the URL + `/slack/events`

## 🔧 Local Development

### Option 1: Docker Compose (Recommended)

1. **Install Docker and Docker Compose**
2. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your Slack credentials
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **For testing with ngrok**:
   ```bash
   # In another terminal
   ngrok http 5000
   ```

5. **Use the ngrok URL** in Slack app configuration:
   - Request URL: `https://your-ngrok-url.ngrok.io/slack/events`

### Option 2: Direct Docker

```bash
# Build the image
docker build -t status-bot .

# Run the container
docker run -p 5000:5000 \
  -e SLACK_BOT_TOKEN=your-token \
  -e SLACK_SIGNING_SECRET=your-secret \
  -e LLM_PROVIDER=ollama \
  status-bot
```

### Option 3: Local Python (without Ollama)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SLACK_BOT_TOKEN=your-token
export SLACK_SIGNING_SECRET=your-secret
export LLM_PROVIDER=openai  # or local

# Run locally
python app_http.py
```

## 📋 Slack App Configuration

### Required Settings:

1. **Slash Commands**:
   - Command: `/status_msg`
   - Request URL: `https://your-deployed-url.com/slack/events`
   - Short Description: "Generate funny status messages"

2. **Event Subscriptions**:
   - Request URL: `https://your-deployed-url.com/slack/events`
   - Subscribe to: `app_mention`

3. **OAuth & Permissions**:
   - Bot Token Scopes:
     - `chat:write`
     - `commands`

4. **Install App** to your workspace

## 🔍 Testing Your Deployment

1. **Health Check**: Visit `https://your-url.com/health`
2. **Home Page**: Visit `https://your-url.com/`
3. **Test in Slack**: Try `/witty_status busy`

## 🛠️ Troubleshooting

### Common Issues:

1. **"URL verification failed"**:
   - Ensure your URL is publicly accessible
   - Check that the endpoint returns 200 OK
   - Verify SSL certificate (https://)

2. **"Command not found"**:
   - Check that the slash command is properly configured
   - Verify the app is installed to your workspace
   - Check bot token permissions

3. **"LLM not working"**:
   - Check environment variables
   - Verify API keys are correct
   - Check logs for specific errors

### Environment Variables Checklist:

```bash
# Required
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# LLM Configuration (choose one)
LLM_PROVIDER=openai  # or local, ollama
OPENAI_API_KEY=your-openai-key  # if using OpenAI
LOCAL_MODEL_NAME=distilbert-base-uncased  # if using local
OLLAMA_BASE_URL=http://localhost:11434  # if using Ollama
OLLAMA_MODEL=llama2:7b  # if using Ollama
```

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Ease of Use | Docker Support |
|----------|-----------|------------|-------------|----------------|
| Railway | ✅ 500 hours/month | $5/month | ⭐⭐⭐⭐⭐ | ✅ |
| Render | ✅ 750 hours/month | $7/month | ⭐⭐⭐⭐ | ✅ |
| Heroku | ❌ | $7/month | ⭐⭐⭐ | ✅ |
| DigitalOcean | ❌ | $5/month | ⭐⭐⭐ | ✅ |

## 🎯 Recommended Setup

For beginners: **Railway** with **Docker + Ollama**
- Easiest deployment
- Completely self-contained
- No API costs
- Professional LLM capabilities

For cost-conscious: **Render** with **Docker + Ollama**
- Generous free tier
- No API costs
- Full containerization
