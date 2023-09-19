"""Welcome to Reflex! This file outlines the steps to create a basic app."""

# Import reflex.
# import openai
import reflex as rx
from chatbot.state import Message, State

# Define views.
def header():
    """Basic instructions to get started."""
    return rx.box(
        rx.text("Assistance 🫶", font_size="2rem"),
        rx.text(
            "Please input something to find out.",
            margin_top="0.5rem",
            color="#666",
        ),
    )


def message(message: Message):
    return rx.box(
        rx.text(
            message.title, 
            font_weight="bold",
            font_size="2em",
        ),
        rx.markdown(
            message.text
        ),
        width="100%",
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
    )


def assist():
    return rx.box(
        rx.input(
            placeholder="Text to Question",
            on_change=State.set_question,
            margin_top="1rem",
            border_color="#eaeaef"
        ),
        rx.button(
            "Post", on_click=State.post, margin_top="1rem", align_item="right"
        )
    )
    

def index():
    """The main view."""
    return rx.container(
        header(),
        rx.vstack(
            rx.foreach(State.messages, message),
            margin_top='2rem',
            spsacing='1rem',
            width="100%"
        ),
        rx.cond(
            State.is_working,
            rx.spinner(
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
app = rx.App(state=State)
app.add_page(index, title="카카오싱크 어시스트")
app.compile()
