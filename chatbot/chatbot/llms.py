from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts.chat import ChatPromptTemplate

INTENT_PROMPT_TEMPLATE = '/datas/prompts/intent/prompt.txt'
INTENT_LIST_TEMPLATE = '/datas/prompts/intent/list.txt'
WITH_DOCS_PROMPT_TEMPLATE = '/datas/prompts/default.txt'
CODE_EXAMPLE_PROMPT_TEMPLATE = '/datas/prompts/with_docs.txt'

llm = ChatOpenAI(temperature=0, max_tokens=16384, model="gpt-3.5-turbo-16k")

def _read_prompt_template(file_path: str) -> str:
    with open(file_path, "r") as f:
        prompt_template = f.read()

    return prompt_template

def _create_chain(llm, template_path, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            template=_read_prompt_template(template_path)
        ),
        output_key=output_key,
        verbose=True,
    )

# llm chains
parse_intent_chain = _create_chain(
    llm=llm,
    template_path=INTENT_PROMPT_TEMPLATE,
    output_key="intent",
)

with_docs_chain = _create_chain(
    llm=llm, 
    template_path=WITH_DOCS_PROMPT_TEMPLATE,
    output_key="answer",
)

code_example_chain = _create_chain(
    llm=llm, 
    template_path=CODE_EXAMPLE_PROMPT_TEMPLATE,
    output_key="answer",
)

default_chain = ConversationChain(llm=llm, output_key="answer")