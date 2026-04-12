def grade_task_easy(env_instance):
    """
    Task: "Order a medium Margherita pizza."
    Score is strictly between 0 and 1 (exclusive) as required by OpenEnv.
    - 0.9 if checked out successfully with correct pizza (d1, medium)
    - 0.6 if correct item is in cart (not yet checked out)
    - 0.4 if on dominos platform at least
    - 0.1 baseline partial credit
    """
    # Successful checkout with correct item
    if env_instance.status == "success":
        for item in env_instance.cart:
            if item["product"]["id"] == "d1" and item["variant"] == "medium":
                return 0.9
        # Checked out but wrong item
        return 0.5

    # Correct item in cart (not checked out yet)
    for item in env_instance.cart:
        if item["product"]["id"] == "d1" and item["variant"] == "medium":
            return 0.6

    # Selected but not in cart
    if env_instance.selected_product:
        if env_instance.selected_product["product"]["id"] == "d1" and env_instance.selected_product["variant"] == "medium":
            return 0.5

    # At least on the right platform
    if env_instance.current_platform == "dominos":
        return 0.4

    return 0.1


def grade_task_medium(env_instance):
    """
    Task: "Order a paperback copy of Atomic Habits and a 30W iPhone 15 charger."
    Score is strictly between 0 and 1 (exclusive) as required by OpenEnv.
    """
    has_book = any(item["product"]["id"] == "a3" and item["variant"] == "paperback" for item in env_instance.cart)
    has_charger = any(item["product"]["id"] == "a1" and item["variant"] == "30W" for item in env_instance.cart)
    items_in_cart = sum([has_book, has_charger])
    
    if env_instance.status == "success":
        if items_in_cart == 2: return 0.9
        if items_in_cart == 1: return 0.7
        return 0.4
    
    if items_in_cart == 2: return 0.6
    if items_in_cart == 1: return 0.4
    
    if env_instance.current_platform == "amazon":
        return 0.2
        
    return 0.1


def grade_task_hard(env_instance):
    """
    Task: "Order a large Pepperoni pizza, stuffed Garlic Bread, and 1kg of Oats from flipkart."
    Score is strictly between 0 and 1 (exclusive) as required by OpenEnv.
    """
    has_pizza = any(item["product"]["id"] == "d2" and item["variant"] == "large" for item in env_instance.cart)
    has_bread = any(item["product"]["id"] == "d3" and item["variant"] == "stuffed" for item in env_instance.cart)
    has_oats = any(item["product"]["id"] == "f2" and item["variant"] == "1kg" for item in env_instance.cart)
    items_in_cart = sum([has_pizza, has_bread, has_oats])
    
    if env_instance.status == "success":
        if items_in_cart == 3: return 0.9
        if items_in_cart == 2: return 0.7
        if items_in_cart == 1: return 0.5
        return 0.3
        
    if items_in_cart == 3: return 0.6
    if items_in_cart == 2: return 0.5
    if items_in_cart == 1: return 0.3
    
    if env_instance.current_platform in ["dominos", "flipkart"]:
        return 0.2
        
    return 0.1


TASKS = [
    {
        "id": "task_1_easy",
        "description": "Order a medium Margherita pizza.",
        "grader": grade_task_easy
    },
    {
        "id": "task_2_medium",
        "description": "Order a paperback copy of Atomic Habits and a 30W iPhone 15 charger.",
        "grader": grade_task_medium
    },
    {
        "id": "task_3_hard",
        "description": "Order a large Pepperoni pizza, stuffed Garlic Bread, and 1kg of Oats from flipkart.",
        "grader": grade_task_hard
    }
]
