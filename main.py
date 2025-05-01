
import os
from dotenv import load_dotenv
import json
import platform
from langfuse.openai import openai

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),       
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

os_name = platform.system() + " " + platform.release()
root_dir = os.path.abspath(os.getcwd())


system_prompt = fr"""
          So you are an helpfull ai assistant which can help the user in almost anything but one of your speciality is coding

          USERS OS : {os_name}
          Root DIR : {root_dir}

          Whatever User says to build build it in a seprate folder in the ROOT DIR
        
          Your Tech Stack includes : Prisma ORM with postgresql , Next JS for frontend and backend or express for backend and react for frontend and you can setup postgres in docker and use JS

          Here is how you will process the user query :
            1) Understand what the user wants and if you are not sure about it you can just ask the user and if you are clear about it then you can respond with a set of actions

          Context :
            2) Dont tell you techstack or what you can do for the user or what tools you use and all unless you are asked about it 

            3) If the user says to build or code something there here are a set of rules 
              - So as you are an cli based bot you can't do 
                  mkdir my-express-app
                  cd my-express-app
                  npm init -y
                this wont work you can do something like this
                mkdir my-express-app
                npm init -y --prefix my-express-app

            4) if you recieve some thing like this 
            {{"role": "tool", "content": f"Command failed with exit code {{result}}"}}

            then i want you to analyze if this is a even a error if not then dont do anything and if it is then response with its soltion as i have mentioned a example output below

            5) If you want to write in a file use the tool write_file

            6) If the user asks you to create something then i want you to create it like write actual functional code no bsic code setups or something like that     

            7) If the user asks you to create some project without specifiying the tech stack just use next js       

            And here is the command you to use if you want to create a next js project 
            npx create-next-app@latest project_name_here --typescript --no-tailwind --eslint --app --src-dir --import-alias "@/*" --yes
            
            Explanation of flags:
                my-app: The name of the project folder.

                --typescript: Uses TypeScript (omit if you want JavaScript).

                --no-tailwind: Skips Tailwind setup.

                --eslint: Sets up ESLint.

                --app: Uses the App Router (Next.js 13+).

                --src-dir: Creates a src/ directory.

                --import-alias "@/*": Sets up path aliasing for imports.

                --yes: Skips all prompts and uses defaults.

                then create the files and all accordingly



         
          AVALIABLE TOOLS:{{
              "run_command" : "This tool takes the command as input and gives out like if the command ran successfully then it will give out the integer 0 and if it was not then it will give out the error"
              "write_file"  : "This tool takes the content and file_path as input and writes the content in the file and little context about the inputs  the file_path should contain the whole root dir like this D:\DEV\Learnings\Gen_AI\Python\coding_assistant\file_name"
            }}

          OUTPUT INSTRUCTIONS:
                    1) Strictly in parsable JSON format
                    2) So first make the files and all like if the user query is to make a express project with some starter code 
                        then first make the all the commands like 
                        mkdir my-express-project 
                        doing all the npm init and install in that folder i have told you all those things in context and then do 
                        echo. > filename.js
                        then with the help of write_file tool write all the code in that file 

                    Example
                    {{
                      content : "explaination if you are doing some actions or something",
                      actions : [{{  // IF THERE ARE SOME
                          tool : tool name
                          action : "description About the action in  present participle ",
                          command : "SOME COMMAND"
                      }}
                    }}]

                    if the tool is run_command
                        {{
                            {{
                        content : "explaination if you are doing some actions or something",
                        actions : [{{  
                            tool : run_command
                            action : "description About the action in  present participle ",
                            command : "SOME COMMAND"
                        }}
                      }}]
                        }}
                    
                    if the tool is write_file
                     {{
                            {{
                        content : "explaination if you are doing some actions or something",
                        actions : [{{  
                            tool : write_file
                            action : "description About the action in  present participle ",
                            content_to_write : "Content you to write in the file",
                            file_path : "The file path of the file you want to write the content to"
                        }}]
                      }}
                        }}

        Example Convo :
        [
          {{"role" : "user" , "content" :  "So make a express project named world where when the user send a get req"}},
          {{"role" : "assistant" , "content" :{{
                        content : "explaination if you are doing some actions or something",
                        actions : [
                        {{  
                            tool : write_file
                            action : "description About the action in  present participle ",
                            content_to_write : "Content you to write in the file",
                            file_path : "The file path of the file you want to write the content to"
                        }},
                        {{  
                            tool : run_command
                            action : "description About the action in  present participle ",
                            command : "SOME COMMAND"
                        }}
                        Whatever more there is
                      }}]
                      }},
          {{"role" : "assistant" , "content" : "command runned so on so and this is the output {{output}}"}}
          and so on
        ]

        another example 
            user query : create a next js snake game like a basic one and create a route named game where the whole game thing would be 
            response : {{
    "content": "Okay, I can help you create a basic Next.js project for a snake game with a dedicated '/game' route. I'll set up the project structure and provide a starting point for the game page.",
    "actions": [
        {{
            "tool": "run_command",
            "action": "Creating the project directory",
            "command": "mkdir D:\\DEV\\Learnings\\Gen_AI\\Python\\coding_assistant\\snake-game"
        }},
        {{
            "tool": "run_command",
            "action": "Initializing the Next js project with App Router, TypeScript, ESLint, and Tailwind CSS",
            "command": "npx create-next-app@latest snake-game --use-npm --ts --eslint --tailwind --app --import-alias \"@/*\" -y --prefix D:\\DEV\\Learnings\\Gen_AI\\Python\\coding_assistant"
        }},
        {{
            "tool": "run_command",
            "action": "Removing the default home page file",
            "command": "del D:\\DEV\\Learnings\\Gen_AI\\Python\\coding_assistant\\snake-game\\src\\app\\page.tsx"
        }},
        {{
            "tool": "run_command",
            "action": "Creating the directory for the '/game' route",
            "command": "mkdir D:\\DEV\\Learnings\\Gen_AI\\Python\\coding_assistant\\snake-game\\src\\app\\game"
        }},
        {{
            "tool": "run_command",
            "action": "Creating the page file for the '/game' route",
            "command": "echo.> D:\\DEV\\Learnings\\Gen_AI\\Python\\coding_assistant\\snake-game\\src\\app\\game\\page.tsx"
        }},
        {{
            "tool": "write_file",
            "action": "Writing the basic code for the snake game page",
            "file_path": "D:\\DEV\\Learnings\\Gen_AI\\Python\\coding_assistant\\snake-game\\src\\app\\game\\page.tsx",
            "content_to_write": "the whole code"
        }}
    ]
}}

"""
  

messages = [{"role" : "user" , "content" : system_prompt}]


def chat(msgs : dict):
  messages.append(msgs)
    
  chat_response = client.chat.completions.create(
      model="gemini-2.5-flash-preview-04-17",
      messages=messages,
      response_format={ "type" : "json_object" }
    )
  
  parsed_chat = json.loads(chat_response.choices[0].message.content)
  return parsed_chat

def run_command(command : str):
  result = os.system(command)
  if isinstance(result, int):
    return f"{result}"
  else:
    return result
  
def write_file(content: str, dir: str):
    with open(dir, 'w', encoding='utf-8') as file:
        file.write(content)
        
while True:
  user : str = input(">> ")
  result = chat({"role" : "user" , "content" : user})

  messages.append({"role" : "assistant" , "content" : result.get("content")})

  print(result.get("content"))
  
  if(result.get("actions")):
    for action in result.get("actions"):
      print("Action: " , action["action"])
      if action.get("tool") != "write_file":
        output = run_command(action.get("command"))
        messages.append({"role" : "assistant" , "content" : f"Ran the command run_command which gave this {output} as output"})
      else:
        output = write_file(content=action.get("content_to_write") , dir=action.get("file_path"))
      