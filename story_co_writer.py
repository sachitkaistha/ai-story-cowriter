key = "your_api_key"
from openai import OpenAI
import gradio as gr
from gtts import gTTS
import tempfile

# Initialize Gemini model
gemini_model = OpenAI(api_key=key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

# Mood prefix map (to simulate tone)
mood_prefix = {
    "Mystery": "In a whisper filled with suspense,",
    "Fantasy": "With a magical sparkle,",
    "Romance": "In a soft and loving voice,"
}

# Story continuation function
def continue_story(user_sentence, mood):
    if not user_sentence.strip():
        return "Please enter a sentence to continue the story.", None

    system_prompt = f"You are a creative storyteller. Continue the user's sentence in a {mood.lower()} tone. Add one imaginative paragraph only."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_sentence.strip()}
    ]

    response = gemini_model.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )
    ai_sentence = response.choices[0].message.content.strip()

    # Add mood prefix to simulate tone in TTS
    spoken_sentence = f"{mood_prefix[mood]} {ai_sentence}"

    # Create TTS
    tts = gTTS(spoken_sentence)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_path = fp.name

    return ai_sentence, audio_path

# Gradio interface
gr.Interface(
    fn=continue_story,
    title="📖 Story Co-Writer ✨",
    description=(
        "Write a sentence and let the AI continue it in a chosen tone! 🎭\n\n"
        "✨ Moods: Mystery (suspense), Fantasy (magical), Romance (warm).\n"
        "🔊 Listen to how the story sounds in that emotion!"
    ),
    inputs=[
        gr.Textbox(label="Your Sentence", placeholder="Start your story here..."),
        gr.Radio(["Mystery", "Fantasy", "Romance"], label="Select Story Mood", value="Mystery")
    ],
    outputs=[
        gr.Textbox(label="AI Continues..."),
        gr.Audio(label="Audio", type="filepath")
    ],
    live=False,
    allow_flagging="never"
).launch()
