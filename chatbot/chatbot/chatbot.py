"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# import openai
import pynecone as pc
from chatbot.state import Message, State

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


def message(message: Message):
    return pc.box(
        pc.text(
            message.title, 
            font_weight="bold",
            font_size="2em",
        ),
        pc.markdown(
            message.text
        ),
        width="100%",
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
    )


def assist():
    return pc.box(
        pc.input(
            placeholder="Text to Question",
            on_blur=State.set_question,
            margin_top="1rem",
            border_color="#eaeaef"
        ),
        pc.button(
            "Post", on_click=State.post, margin_top="1rem", align_item="right"
        )
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
        pc.cond(
            State.is_working,
            pc.spinner(
                color="lightgreen",
                thickness=5,
                speed="1.5s",
                size="xl",
            )
        ),
        assist(),
        padding="2rem",
        max_width="1024px"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="카카오싱크 어시스트")
app.compile()
