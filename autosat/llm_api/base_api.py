import openai
import requests


class BaseCallAPI():
    def __init__(self, api_base, api_key, model_name):
        self.api_base = api_base
        self.api_key = api_key
        openai.api_base = self.api_base
        openai.api_key = self.api_key
        self.model_name = model_name

    def load_prompt(self, file_dir):
        with open(file_dir, 'r') as file:
            prompt = file.read()
        return prompt

    def call_api(self, prompt, temperature):
        pass


class GPTCallAPI(BaseCallAPI):
    def __init__(self, api_base, api_key, model_name, stream):
        super(GPTCallAPI, self).__init__(api_base, api_key, model_name)
        self.stream = stream

    def call_api(self, prompt_file, temperature=0.2):
        with open(prompt_file, 'r') as file:
            prompt = file.read()
        response = openai.ChatCompletion.create(
            model=self.model_name,
            # model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chatbot", },
                {"role": "user", "content": prompt}],
            temperature=temperature,
            stream=self.stream
        )

        if self.stream:
            result = ""
            try:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        result += chunk.choices[0].delta.content
                        # print(chunk.choices[0].delta.content, end="")
            except:
                pass
        else:
            result = response["choices"][0]["message"]["content"]

        return result

    def call_api_prompt(self, prompt, temperature=0.2):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a chatbot", },
                {"role": "user", "content": prompt}],
            temperature=temperature,
            stream=self.stream
        )

        if self.stream:
            result = ""
            try:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        result += chunk.choices[0].delta.content
                        print("哈哈",chunk.choices[0].delta.content, end="")
            except:
                pass
        else:
            result = response["choices"][0]["message"]["content"]

        return result

class LocalCallAPI(BaseCallAPI):
    def __init__(self, api_base, api_key, model_name):
        super(LocalCallAPI, self).__init__(api_base, api_key, model_name)

    def call_api(self, prompt_file,
                 temperature=0.2):
        stop_tokens = ["<|im_end|>"]
        system_prompt = "You are a chatbot"

        with open(prompt_file, 'r') as file:
            prompt = file.read()

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}],
                stop=stop_tokens)
        return response["choices"][0]["message"]["content"]

class QwenCallAPI(BaseCallAPI):
    def __init__(self, api_base, api_key, model_name,stream):
        super(QwenCallAPI, self).__init__(api_base, api_key, model_name)
        self.stream = stream
    def call_api(self, prompt_file, temperature=0.2):
        system_prompt = "You are a helpful assistant."

        with open(prompt_file, 'r') as file:
            user_prompt = file.read()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        body = {
            'model': "deepseek-chat",
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message",
                "temperature": temperature
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.post(self.api_base, headers=headers, json=body)
        response_json = response.json()

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response_json}")
        return response_json['output']['choices'][0]['message']['content']

    def call_api_prompt(self, prompt, temperature=0.2):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a chatbot", },
                {"role": "user", "content": prompt}],
            temperature=temperature,
            stream=self.stream
        )

        if self.stream:
            result = ""
            try:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        result += chunk.choices[0].delta.content

            except:
                pass
        else:
            result = response["choices"][0]["message"]["content"]

        return result
class ZhiPuCallAPI(BaseCallAPI):
    def __init__(self, api_base, api_key, model_name):
        super(ZhiPuCallAPI, self).__init__(api_base, api_key, model_name)

    def call_api(self, prompt_file, temperature=0.2):
        system_prompt = "You are a helpful assistant."

        with open(prompt_file, 'r', encoding='utf-8') as file:
            user_prompt = file.read()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        body = {
            'model': "glm-4-plus",
            'messages': messages
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        url = f"{self.api_base}/api/paas/v4/chat/completions"
        response = requests.post(url, headers=headers, json=body)
        response_json = response.json()

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response_json}")
        # return response_json
        return response_json['choices'][0]['message']['content']

    def call_api_prompt(self, prompt,
                        temperature=0.2):
        system_prompt = "You are a helpful assistant."


        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        body = {
            'model': "glm-4-plus",
            'messages': messages
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        url = f"{self.api_base}/api/paas/v4/chat/completions"
        response = requests.post(url, headers=headers, json=body)
        response_json = response.json()

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response_json}")
        # return response_json
        return response_json['choices'][0]['message']['content']
def fastllm(prompt , args):
    if args.llm_model == "gpt-4-turbo":
        llm_api = GPTCallAPI(api_base=args.api_base,
                             api_key=args.api_key,
                             model_name=args.llm_model,
                             stream=False)
    elif args.llm_model == "gpt-3.5-turbo":
        llm_api = GPTCallAPI(api_base=args.api_base,
                             api_key=args.api_key,
                             model_name=args.llm_model)
    elif args.llm_model in ('Qwen', 'llama','deepseek-chat', 'stream=False'):
        llm_api = QwenCallAPI(api_base=args.api_base,
                              api_key=args.api_key,
                              model_name=args.llm_model,
                              stream=False)
    elif args.llm_model in ('zhipu'):
        llm_api = ZhiPuCallAPI(api_base=args.api_base,
                               api_key=args.api_key,
                               model_name=args.llm_model)

    answer = llm_api.call_api_prompt(prompt=prompt, temperature=args.temperature)
    return answer
if __name__ == '__main__':
    llm_api = ZhiPuCallAPI(api_base="https://open.bigmodel.cn",
                          api_key="deb51660770a451ee5e563b8777e58d2.DNPy2TBymys07H73",
                          model_name="glm-4-plus")
    answer = llm_api.call_api(prompt_file=r'D:\Desktop\AutoSAT-master\examples\EasySAT\rephase_function\original_prompt.txt')
    print(answer)
