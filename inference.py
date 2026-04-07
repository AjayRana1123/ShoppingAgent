import os
import json
from openai import OpenAI
from env import ShoppingEnv
from tasks_and_graders import TASKS

def run_inference():
    print("[START] Starting inference run")
    
    API_BASE_URL = os.getenv("API_BASE_URL","https://router.huggingface.co/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    if not HF_TOKEN:
        print("[END] HF_TOKEN not set")
        return
        
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )
    
    environment = ShoppingEnv(dataset_path="dataset.json")
    
    for task_idx, task_spec in enumerate(TASKS):
        print(f"\n[STEP] Running Task: {task_spec['description']}")
        
        state = environment.reset(task_spec["description"])
        done = False
        step_count = 0
        
        messages = [
            {"role": "system", "content": "You are an autonomous shopping agent. You must exclusively output valid JSON without markdown formatting. CRITICAL INSTRUCTION: Once you have successfully fulfilled the user's request (e.g. added the target item to your cart), you MUST immediately execute the 'checkout' action to finish the task. Do not repeat actions."}
        ]
        
        while not done and step_count < 10:
            state_prompt = f"""
Current task: {state["user_request"]}
Available platforms: {state["available_platforms"]}
Current platform: {state["current_platform"]}
Search results: {state["search_results"]}
Selected product: {state["selected_product"]}
Cart: {state["cart"]}
Budget: {state["budget"]}

Possible actions:
1. {{"type": "choose_platform", "platform": "platform_name"}}
2. {{"type": "search_product", "query": "search term"}}
3. {{"type": "select_product", "product_id": "id", "variant": "variant_name"}}
4. {{"type": "add_to_cart"}}
5. {{"type": "checkout"}}
"""
            messages.append({"role": "user", "content": state_prompt})
            
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.0
                )
                
                content = response.choices[0].message.content
                action = json.loads(content)
                messages.append({"role": "assistant", "content": content})
                print(f"[STEP] Agent decided action: {action}")
                
            except Exception as e:
                print(f"[STEP] LLM or parsing error: {e}")
                action = {"type": "invalid"}
            
            state, reward, done, msg = environment.step(action)
            messages.append({"role": "user", "content": f"Env feedback: {msg}"})
            print(f"[STEP] Env feedback: {msg}")
            step_count += 1
            
        final_score = task_spec["grader"](environment)
        print(f"[STEP] Task completed. Status: {state['status']}. Score: {final_score}")
        
    print("[END] Inference complete")

if __name__ == "__main__":
    run_inference()
