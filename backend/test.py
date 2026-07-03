import asyncio
from openai import AsyncOpenAI

async def test():
    client = AsyncOpenAI(api_key='AIzaSyATGG1XCEQDylZnWZnyfu0WOCCs7UPOHQY', base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
    try:
        response = await client.chat.completions.create(
            model='gemini-2.0-flash',
            messages=[{'role': 'user', 'content': 'hi'}]
        )
        print("Success 2.0-flash:", response)
    except Exception as e:
        print("Error 2.0-flash:", e)
        
    try:
        response = await client.chat.completions.create(
            model='gemini-1.5-pro',
            messages=[{'role': 'user', 'content': 'hi'}]
        )
        print("Success 1.5-pro:", response)
    except Exception as e:
        print("Error 1.5-pro:", e)

asyncio.run(test())
