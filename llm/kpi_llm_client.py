import os
import json
from openai import OpenAI
import ollama
from llm.kpi_prompt import KPI_LLM_SYSTEM_PROMPT


class KPI_LLM_Client:

    @staticmethod
    def get_client():
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            return OpenAI(api_key=api_key)
        return None

    @staticmethod
    def parse(query: str):
        client = KPI_LLM_Client.get_client()
        
        if client:
            try:
                print("Using OpenAI for parsing...")
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": KPI_LLM_SYSTEM_PROMPT},
                        {"role": "user", "content": query}
                    ]
                )
                content = response.choices[0].message.content
                return json.loads(content)
            except Exception as e:
                print(f"OpenAI error: {e}. Falling back to Ollama...")

        # Fallback to Ollama
        try:
            print("Using Ollama (llama3) for parsing...")
            response = ollama.chat(
                model='llama3',
                messages=[
                    {'role': 'system', 'content': KPI_LLM_SYSTEM_PROMPT},
                    {'role': 'user', 'content': query},
                ]
            )
            content = response['message']['content']
            
            # Clean up potential markdown from Ollama
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            raise Exception(f"Failed to parse KPI with both OpenAI and Ollama: {e}")