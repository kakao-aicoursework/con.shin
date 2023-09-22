import pynecone as pc
from pynecone.base import Base

from chatbot.dataloader import EmbeddingDB
from chatbot.llms import default_chain, with_docs_chain, parse_intent_chain, INTENT_LIST_TEMPLATE, code_example_chain

embedding_db = EmbeddingDB()

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
    answer = ""
    context = dict(input=question)
    context["intent_list"] = read_prompt_template(INTENT_LIST_TEMPLATE)
    intent = parse_intent_chain.run(context)

    if intent == "API 이해" or intent == "질문 답변":
        context["related_documents"] = embedding_db.get_page_contents(question)
        answer = with_docs_chain.run(context)

    elif intent == "버그 수정" or intent == "사용 예시":
        # Tool 사용해서 Web Search
        answer = code_example_chain.run(context)
    else:
        answer = default_chain.run(context["input"])

    return answer

class State(pc.State):
    """The app state."""
    is_working: bool = False
    question: str = ""
    messages: list[Message] = []
    current_idx: int = 0

    @pc.var
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