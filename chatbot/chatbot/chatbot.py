"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# Import pynecone.
# import openai
import os
import pynecone as pc
from pynecone.base import Base

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain

os.environ["OPENAI_API_KEY"] = "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"
# openai.api_key = os.environ.get('OPENAI_API_KEY')

def read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()

    return prompt_template

def question_to_chatgpt(question: str) -> str:
    writer_llm = ChatOpenAI(temperature=1, max_tokens=8192, model='gpt-3.5-turbo-16k')
    writer_prompt_template = ChatPromptTemplate.from_template(
        template=read_prompt_template('project_data_카카오싱크.txt'))
    writer_chain = LLMChain(llm=writer_llm, prompt=writer_prompt_template, output_key='output')

    result = writer_chain(dict(
        question=question,
    ))

    return result['output']
    
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
    is_working: bool = False
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

    async def post(self):
        self.is_working = True
        yield

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
        self.is_working = False
        self.text = ""
        yield


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
            on_blur=State.set_text,
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
        pc.cond(State.is_working,
                    pc.spinner(
                        color="lightgreen",
                        thickness=5,
                        speed="1.5s",
                        size="xl",
                    ),),
        header(),
        pc.vstack(
            pc.foreach(State.messages, message),
            margin_top='2rem',
            spsacing='1rem',
            width="100%"
        ),
        assist(),
        padding="2rem",
        max_width="1024px"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="카카오싱크 어시스트")
app.compile()
