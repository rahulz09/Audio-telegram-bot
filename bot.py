import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import config
from services import GoogleTTSService, ElevenLabsTTSService

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize TTS services
google_tts = GoogleTTSService()
elevenlabs_tts = ElevenLabsTTSService()

# User settings storage (in production, use a database)
user_settings = {}


def get_user_settings(user_id: int) -> dict:
    """Get or create user settings"""
    if user_id not in user_settings:
        user_settings[user_id] = {
            "model": config.DEFAULT_MODEL,
            "google_voice": config.DEFAULT_GOOGLE_VOICE,
            "elevenlabs_voice": config.DEFAULT_ELEVENLABS_VOICE
        }
    return user_settings[user_id]


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Create main menu keyboard"""
    keyboard = [
        ["🎤 Voice Select", "⚙️ Settings"],
        ["🔊 Model Select", "ℹ️ Help"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with main menu"""
    user = update.effective_user
    get_user_settings(user.id)  # Initialize user settings

    welcome_message = (
        f"🎙️ *Welcome {user.first_name}!*\n\n"
        "Main YouTube script ko audio mein convert kar sakta hoon!\n\n"
        "📝 *Kaise use karein:*\n"
        "1. Apna script paste karein\n"
        "2. Main audio bana kar bhej dunga\n\n"
        "🎛️ *Menu Options:*\n"
        "• 🎤 Voice Select - Voice badlein\n"
        "• ⚙️ Settings - Current settings dekhein\n"
        "• 🔊 Model Select - TTS model chunein\n"
        "• ℹ️ Help - Help dekhein\n\n"
        "_Bas apna script paste karein aur audio paayein!_"
    )

    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message"""
    help_text = (
        "📖 *Help Guide*\n\n"
        "*Available Commands:*\n"
        "/start - Bot shuru karein\n"
        "/help - Ye help message\n"
        "/settings - Current settings\n"
        "/voice - Voice select karein\n"
        "/model - TTS model select karein\n\n"
        "*Models Available:*\n"
        "• Google TTS - Fast & reliable\n"
        "• ElevenLabs - High quality voices\n\n"
        "*How to use:*\n"
        "1. Model select karein\n"
        "2. Voice select karein\n"
        "3. Apna script paste karein\n"
        "4. Audio receive karein!\n\n"
        "_Script max 4096 characters tak ho sakta hai._"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current user settings"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)

    current_model = config.TTS_MODELS.get(settings["model"], "Unknown")

    if settings["model"] == "google":
        current_voice = config.GOOGLE_VOICES.get(settings["google_voice"], "Unknown")
    else:
        current_voice = config.ELEVENLABS_VOICES.get(settings["elevenlabs_voice"], "Unknown")

    settings_text = (
        "⚙️ *Current Settings*\n\n"
        f"🔊 *Model:* {current_model}\n"
        f"🎤 *Voice:* {current_voice}\n\n"
        "_Use menu buttons to change settings_"
    )
    await update.message.reply_text(settings_text, parse_mode="Markdown")


async def model_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show model selection menu"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)

    keyboard = []
    for model_key, model_name in config.TTS_MODELS.items():
        # Add checkmark for selected model
        prefix = "✅ " if settings["model"] == model_key else ""
        keyboard.append([
            InlineKeyboardButton(
                f"{prefix}{model_name}",
                callback_data=f"model_{model_key}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔊 *Select TTS Model:*\n\n"
        "Choose your preferred Text-to-Speech model:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def voice_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show voice selection menu based on current model"""
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)

    if settings["model"] == "google":
        voices = config.GOOGLE_VOICES
        current_voice = settings["google_voice"]
        callback_prefix = "gvoice"
    else:
        voices = config.ELEVENLABS_VOICES
        current_voice = settings["elevenlabs_voice"]
        callback_prefix = "evoice"

    keyboard = []
    for voice_id, voice_name in voices.items():
        prefix = "✅ " if voice_id == current_voice else ""
        keyboard.append([
            InlineKeyboardButton(
                f"{prefix}{voice_name}",
                callback_data=f"{callback_prefix}_{voice_id}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    model_name = config.TTS_MODELS.get(settings["model"], "Unknown")

    await update.message.reply_text(
        f"🎤 *Select Voice for {model_name}:*\n\n"
        "Choose your preferred voice:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    settings = get_user_settings(user_id)
    data = query.data

    if data.startswith("model_"):
        # Handle model selection
        model = data.replace("model_", "")
        settings["model"] = model
        model_name = config.TTS_MODELS.get(model, "Unknown")

        await query.edit_message_text(
            f"✅ *Model Selected:* {model_name}\n\n"
            "_Ab 🎤 Voice Select se voice chunein_",
            parse_mode="Markdown"
        )

    elif data.startswith("gvoice_"):
        # Handle Google voice selection
        voice = data.replace("gvoice_", "")
        settings["google_voice"] = voice
        voice_name = config.GOOGLE_VOICES.get(voice, "Unknown")

        await query.edit_message_text(
            f"✅ *Voice Selected:* {voice_name}\n\n"
            "_Ab apna script paste karein!_",
            parse_mode="Markdown"
        )

    elif data.startswith("evoice_"):
        # Handle ElevenLabs voice selection
        voice = data.replace("evoice_", "")
        settings["elevenlabs_voice"] = voice
        voice_name = config.ELEVENLABS_VOICES.get(voice, "Unknown")

        await query.edit_message_text(
            f"✅ *Voice Selected:* {voice_name}\n\n"
            "_Ab apna script paste karein!_",
            parse_mode="Markdown"
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages - convert to audio"""
    text = update.message.text

    # Check for menu button clicks
    if text == "🎤 Voice Select":
        await voice_select(update, context)
        return
    elif text == "⚙️ Settings":
        await show_settings(update, context)
        return
    elif text == "🔊 Model Select":
        await model_select(update, context)
        return
    elif text == "ℹ️ Help":
        await help_command(update, context)
        return

    # Process script text
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)

    # Check text length
    if len(text) > 4096:
        await update.message.reply_text(
            "❌ Script bahut lamba hai!\n"
            "Maximum 4096 characters allowed.\n\n"
            f"_Aapka script: {len(text)} characters_",
            parse_mode="Markdown"
        )
        return

    # Send processing message
    processing_msg = await update.message.reply_text(
        "🔄 *Processing...*\n\n"
        "_Audio generate ho raha hai, please wait..._",
        parse_mode="Markdown"
    )

    try:
        # Generate audio based on selected model
        if settings["model"] == "google":
            voice = settings["google_voice"]
            audio_path = await google_tts.synthesize(text, voice)
            voice_name = config.GOOGLE_VOICES.get(voice, "Unknown")
        else:
            voice = settings["elevenlabs_voice"]
            audio_path = await elevenlabs_tts.synthesize(text, voice)
            voice_name = config.ELEVENLABS_VOICES.get(voice, "Unknown")

        # Send audio file
        with open(audio_path, "rb") as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                title="Script Audio",
                performer=voice_name,
                caption=(
                    f"🎙️ *Audio Generated!*\n\n"
                    f"🔊 Model: {config.TTS_MODELS.get(settings['model'])}\n"
                    f"🎤 Voice: {voice_name}"
                ),
                parse_mode="Markdown"
            )

        # Delete processing message
        await processing_msg.delete()

        # Clean up temp file
        os.remove(audio_path)

    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        await processing_msg.edit_text(
            f"❌ *Error occurred!*\n\n"
            f"Audio generate karne mein error:\n`{str(e)}`\n\n"
            "_Please try again or contact support._",
            parse_mode="Markdown"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors"""
    logger.error(f"Exception while handling an update: {context.error}")


def main() -> None:
    """Start the bot"""
    # Check for required environment variables
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    # Create application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", show_settings))
    application.add_handler(CommandHandler("voice", voice_select))
    application.add_handler(CommandHandler("model", model_select))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
