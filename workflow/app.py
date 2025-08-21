import gradio as gr
import asyncio
import datetime
from gather_news import gather_news
from workflow import main

# ----- State to track daily gather_news -----
last_gather_date = None

async def handle_submit(recipient_email: str, user_preferences: str):
    global last_gather_date

    today = datetime.date.today()
    if last_gather_date != today:
        # Run once a day
        gather_news()
        last_gather_date = today

    # Now run your async coroutine
    result = await main(recipient_email=recipient_email, prompt=user_preferences)

    # Return result + clear inputs
    return result, "", ""

# ----- Gradio UI -----
with gr.Blocks() as demo:
    gr.Markdown("## Personalized News Digest")

    with gr.Row():
        recipient_email = gr.Textbox(label="Recipient Email")
        user_preferences = gr.Textbox(label="User Preferences", lines=4)

    output = gr.Textbox(label="Output", interactive=False)

    submit_btn = gr.Button("Submit")

    submit_btn.click(
        fn=handle_submit,
        inputs=[recipient_email, user_preferences],
        outputs=[output, recipient_email, user_preferences]
    )

demo.launch()