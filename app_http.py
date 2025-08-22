"""
Slack Status Bot - HTTP Version for Deployment
"""

import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from llm_client import LLMClient
from config import STATUS_TYPES

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = Flask(__name__)

# Initialize Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize LLM client
llm_client = LLMClient()

# Initialize Slack request handler
handler = SlackRequestHandler(app)

@app.command("/witty_status")
def handle_status_command(ack, command):
    """Handle the /witty_status slash command"""
    ack()
    
    try:
        # Parse the command
        text = command.get("text", "").strip().lower()
        user_id = command.get("user_id")
        channel_id = command.get("channel_id")
        
        logger.info(f"Status command received from {user_id}: {text}")
        
        # If no status type provided, show help
        if not text:
            help_text = _get_help_text()
            app.client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=help_text
            )
            return
        
        # Check if status type is valid
        if text not in STATUS_TYPES:
            help_text = _get_help_text()
            app.client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=f"❌ Unknown status type: `{text}`\n\n{help_text}"
            )
            return
        
        # Generate status message
        status_message = llm_client.generate_status(text)
        
        # Post the status message
        response_text = f"🤖 Here's your {text} status:\n\n> *{status_message}*"
        
        app.client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=response_text
        )
        
        logger.info(f"Generated status for {user_id}: {status_message}")
        
    except Exception as e:
        logger.error(f"Error handling status command: {e}")
        app.client.chat_postEphemeral(
            channel=command.get("channel_id"),
            user=command.get("user_id"),
            text="❌ Sorry, something went wrong generating your status message. Please try again."
        )

def _get_help_text():
    """Generate help text for the command"""
    help_text = "📝 *Available status types:*\n"
    for status_type, description in STATUS_TYPES.items():
        help_text += f"• `{status_type}` - {description}\n"
    
    help_text += "\n💡 *Usage:* `/witty_status [type]`\n"
    help_text += "Example: `/witty_status busy`"
    
    return help_text

@app.event("app_mention")
def handle_app_mention(event, say):
    """Handle when the bot is mentioned"""
    say("👋 Hi! I'm the Status Bot. Use `/witty_status [type]` to generate a funny status message!")

# Flask routes
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack events"""
    return handler.handle(request)

@flask_app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "llm_provider": llm_client.provider})

@flask_app.route("/", methods=["GET"])
def home():
    """Home endpoint"""
    return jsonify({
        "message": "StatusSage Bot is running!",
        "llm_provider": llm_client.provider,
        "status_types": list(STATUS_TYPES.keys())
    })

def main():
    """Main function to run the bot"""
    # Test LLM connection
    if llm_client.test_connection():
        logger.info(f"✅ {llm_client.provider} connection successful")
    else:
        logger.warning(f"⚠️  {llm_client.provider} not available, will use template messages")
    
    # Get port from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    logger.info(f"🚀 Starting StatusSage Bot on port {port}...")
    flask_app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
