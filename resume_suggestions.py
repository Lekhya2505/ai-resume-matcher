from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def get_resume_improvement_suggestions(resume_text, jd_text):
    prompt = f"""You are an expert resume consultant. Compare the following resume and job description and provide improvement suggestions:

Resume:
{resume_text}

Job Description:
{jd_text}

Suggestions:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
