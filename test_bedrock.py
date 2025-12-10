from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatBedrock(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-east-1",
)

messages = [
    SystemMessage(content="You are Claude 3.5 Sonnet running on AWS Bedrock."),
    HumanMessage(content="Say hello from Claude 3.5 Sonnet on Bedrock!"),
]

print(llm.invoke(messages).content)