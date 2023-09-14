"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# Import pynecone.
import openai
import os
import pynecone as pc
from pynecone.base import Base


# openai.api_key = "<YOUR_OPENAI_API_KEY>"
openai.api_key = os.environ.get('OPEN_API_KEY')

def question_to_chatgpt(text) -> str:
    messages = [{"role": "user", "content": text}]

    # API 호출
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=messages)
    translated_text = response['choices'][0]['message']['content']
    # Return
    return translated_text


class Message(Base):
    role: str
    align: str
    title: str
    text: str

class UserMessage(Message):
    align = 'left'

class AssistMessage(Message):
    align = 'right'

class State(pc.State):
    """The app state."""
    text: str = ""
    messages: list[Message] = []
    question: list[str] = []
    current_idx: int = 0

    @pc.var
    def output(self) -> str:
        if not self.text.strip():
            return "Translations will appear here."
        answer = question_to_chatgpt(self.text)
        return answer

    def post(self):
        self.messages = self.messages + [
            UserMessage(
                role='user',
                title='user',
                text=self.text,
            ),
            AssistMessage(
                role='assist',
                title='assist',
                text=self.output,
            )
        ]
        self.text = ""


# Define views.
def header():
    """Basic instructions to get started."""
    return pc.box(
        pc.text("Assistance 🫶", font_size="2rem"),
        pc.text(
            "Please input something to find out.",
            margin_top="0.5rem",
            color="#666",
        ),
    )


def down_arrow():
    return pc.vstack(
        pc.icon(
            tag="arrow_down",
            color="#666",
        )
    )


def text_box(text):
    return pc.text(
        text,
        background_color="#fff",
        padding="1rem",
        border_radius="8px",
    )


def message(message: Message):
    return pc.box(
        pc.text(message.title),
        pc.text(
            message.text
        ),
        text_align=message.align,
        width="100%",
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
    )

    


def smallcaps(text, **kwargs):
    return pc.text(
        text,
        font_size="0.7rem",
        font_weight="bold",
        text_transform="uppercase",
        letter_spacing="0.05rem",
        **kwargs,
    )

def assist():
    return pc.box(
        pc.input(
            placeholder="Text to Question",
            on_blur=State.set_text,
            margin_top="1rem",
            border_color="#eaeaef"
        ),
        pc.button(
            "Post", on_click=State.post, margin_top="1rem", align_item="right"
        )
    )
    
def output():
    return pc.box(
        pc.box(
            smallcaps(
                "Output",
                color="#aeaeaf",
                background_color="white",
                padding_x="0.1rem",
            ),
            position="absolute",
            top="-0.5rem",
        ),
        pc.text(State.output),
        padding="1rem",
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )


def index():
    """The main view."""
    return pc.container(
        header(),
        pc.vstack(
            pc.foreach(State.messages, message),
            margin_top='2rem',
            spsacing='1rem',
            width="100%"
        ),
        assist(),
        padding="2rem",
        max_width="600px"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Translator")
app.compile()
