from time import sleep
from openai import OpenAI

client = OpenAI(api_key='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')

assistant = client.beta.assistants.create(
    name="Personal Finance Bot",
    instructions="You are a personal finance bot, you are going to give advice based on users financial goals",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini"
)

#thread
thread = client.beta.threads.create()



while True:
    #inp question
    user_question = input("Please enter your financial question: ")

    
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question
        )
        print("Message sent successfully.")
    except Exception as e:
        print("Error while sending message:", e)
        exit()

    #if run doesn't work
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        print("Run created successfully.")
    except Exception as e:
        print("Error while creating run:", e)
        exit()

    #run status
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print("Run status:", run.status) 
        sleep(1)

    #print response
    try:
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print("Messages retrieved successfully.")
        for message in reversed(messages.data):
            if message.content:
                print(f"{message.role}: {message.content[0].text.value}")
            else:
                print(f"{message.role}: No content")
    except Exception as e:
        print("Error while retrieving messages:", e)

    #another question?
    ask_another = input("Ask another question? (Y/N): ").strip().lower()
    if ask_another != 'y':
        print("Thank you for using the Personal Finance Bot!")
        break
