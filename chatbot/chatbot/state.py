import reflex as rx
from reflex.base import Base

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain

class Message(Base):
    role: str
    align: str
    title: str
    text: str

class UserMessage(Message):
    align = 'left'

class AssistMessage(Message):
    align = 'right'

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

class State(rx.State):
    """The app state."""
    is_working: bool = False
    question: str = ""
    messages: list[Message] = []
    current_idx: int = 0

    @rx.var
    def output(self) -> str:
        if not self.question.strip():
            return "질문을 입력해주세요."
        answer = question_to_chatgpt(self.question)
        return answer

    async def post(self):
        self.is_working = True
        yield
        
        self.messages = self.messages + [
            UserMessage(
                role='user',
                title='user',
                text=self.question,
            ),
            AssistMessage(
                role='assist',
                title='assist',
                text=self.output,
            )
        ]
        self.is_working = False
        self.question = ""
        yield