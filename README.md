---
title: ShoppingAgent
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
tags:
  - openenv
---
# Shopping Agent Environment

This is an autonomous shopping agent simulation designed to model real-world e-commerce task scenarios. The environment exposes standard methods for an agent to interact across multiple platforms, search products, add them to a cart, and execute checkouts.

## Environment Description & Motivation
**Motivation:** Autonomous agents need safe, reproducible playgrounds to practice sequential decision-making without real-world financial consequences. This environment simulates purchasing logic to serve as a robust testing ground for LLM task planning, tool use, and execution parsing.

The `ShoppingEnv` is an interaction ecosystem where an autonomous agent (like an LLM) starts with a specific user task (e.g. "Order a medium Margherita pizza") and a virtual budget. It must navigate through available e-commerce platforms, run queries, and take actions until the user's objectives are fulfilled. 

The environment supports the **OpenEnv Specification**, providing typing via Pydantic models and exposing standard REST endpoints (`/step`, `/reset`, `/state`) using FastAPI.

## Action Space
The agent can interact with the environment by passing JSON actions. The allowed actions are:
- **`choose_platform`**: Switch your active navigation to a provided platform.
   - Example: `{"type": "choose_platform", "platform": "amazon"}`
- **`search_product`**: Queries products on the active platform.
   - Example: `{"type": "search_product", "query": "iphone charger"}`
- **`select_product`**: Selects a specific product and variant from the search results.
   - Example: `{"type": "select_product", "product_id": "a1", "variant": "20W"}`
- **`add_to_cart`**: Puts the actively selected product and variant into your shopping cart.
   - Example: `{"type": "add_to_cart"}`
- **`checkout`**: Completes the order based on the current contents of the shopping cart.
   - Example: `{"type": "checkout"}`

## Observation (State) Space
Upon resetting or taking a step, the environment returns a state containing partial observability attributes:
- **`user_request` (str)**: The current goal string.
- **`available_platforms` (List[str])**: The list of platforms the agent can switch to.
- **`current_platform` (str, optional)**: The platform the agent is actively viewing.
- **`budget` (float)**: Remaining monetary balance.
- **`cart` (List[dict])**: Summary of contents staged for checkout.
- **`search_results` (List[dict])**: The latest retrieved products matching a query.
- **`selected_product` (dict, optional)**: Target product selected for cart inclusion.
- **`status` (str)**: Current episode status (`active`, `success`, `failed`).

## Tasks and Rewards
The environment includes 3 defined objective tasks with custom graders ensuring meaningful partial progress signals:
1. **Easy Task:** Order a medium Margherita pizza. (Reward +1.0 for success)
2. **Medium Task:** Buy a 20W iPhone 15 charger. (Partial reward: +0.5 for reaching Amazon, +0.5 for selecting the correct 20W charger variation)
3. **Hard Task:** Order a large Pepperoni pizza and checkout. (Reward +1.0 for successful d2 large checkout cart validation).

### Baseline Scores
The included baseline agent (`inference.py`) cleanly completes these task definitions when executed utilizing the Meta-Llama-3-8B-Instruct model.
- **Easy Task**: 1.0
- **Medium Task**: 1.0
- **Hard Task**: 1.0

## Setup Instructions

### Environment Variables
Before running the agent offline or in validation, configure your environment with:
- `API_BASE_URL`: The inference API base for your LLM (defaults to OpenAI specs if missed but often `https://router.huggingface.co/v1`).
- `MODEL_NAME`: The string name of the target LLM.
- `HF_TOKEN`: Valid API key/token.

### Local Execution
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run OpenEnv Validation Server (API Server):**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 7860
   ```
3. **Run Baseline Inference Agent (Separately):**
   ```bash
   python inference.py
   ```

### Docker deployment / Hugging Face Spaces
The included `Dockerfile` automatically installs dependencies and starts the FastAPI server natively on standard Spaces port `7860` bridging the simulation endpoint for grader pings.
