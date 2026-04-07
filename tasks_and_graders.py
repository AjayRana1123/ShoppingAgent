def grade_task_easy(env_instance):
    """
    Task: "Order a medium Margherita pizza."
    Reward +1 if platform is Domino's.
    """
    if env_instance.current_platform == "dominos":
        return 1.0
    return 0.0

def grade_task_medium(env_instance):
    """
    Task: "Buy a 20W iPhone 15 charger."
    Reward +0.5 if platform is amazon.
    Reward +1.0 if correct product (a1) and variant (20W) are selected or in cart.
    """
    score = 0.0
    if env_instance.current_platform == "amazon":
        score += 0.5
        
    for item in env_instance.cart:
        if item["product"]["id"] == "a1" and item["variant"] == "20W":
            return 1.0
            
    # Also check if it's selected but not added
    if env_instance.selected_product:
        if env_instance.selected_product["product"]["id"] == "a1" and env_instance.selected_product["variant"] == "20W":
            return 1.0
            
    return score

def grade_task_hard(env_instance):
    """
    Task: "Order a large Pepperoni pizza and checkout."
    Reward +1 only if successfully checked out with d2 (large)
    """
    if env_instance.status == "success":
        for item in env_instance.cart:
            if item["product"]["id"] == "d2" and item["variant"] == "large":
                return 1.0
    return 0.0

TASKS = [
    {
        "id": "task_1_easy",
        "description": "Order a medium Margherita pizza.",
        "grader": grade_task_easy
    },
    {
        "id": "task_2_medium",
        "description": "Buy a 20W iPhone 15 charger.",
        "grader": grade_task_medium
    },
    {
        "id": "task_3_hard",
        "description": "Order a large Pepperoni pizza and checkout.",
        "grader": grade_task_hard
    }
]
