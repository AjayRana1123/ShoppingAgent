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
    Task: "Buy a 20W iPhone 15 charger."
    Score is strictly between 0 and 1 (exclusive) as required by OpenEnv.
    - 0.9 if checked out successfully with correct charger (a1, 20W)
    - 0.7 if correct item is in cart
    - 0.5 if correct item is selected
    - 0.3 if on amazon platform
    - 0.1 baseline partial credit
    """
    # Successful checkout with correct item
    if env_instance.status == "success":
        for item in env_instance.cart:
            if item["product"]["id"] == "a1" and item["variant"] == "20W":
                return 0.9
        return 0.5

    # Correct item in cart
    for item in env_instance.cart:
        if item["product"]["id"] == "a1" and item["variant"] == "20W":
            return 0.7

    # Correct item selected but not in cart
    if env_instance.selected_product:
        if env_instance.selected_product["product"]["id"] == "a1" and env_instance.selected_product["variant"] == "20W":
            return 0.5

    # At least on the right platform
    if env_instance.current_platform == "amazon":
        return 0.3

    return 0.1


def grade_task_hard(env_instance):
    """
    Task: "Order a large Pepperoni pizza and checkout."
    Score is strictly between 0 and 1 (exclusive) as required by OpenEnv.
    - 0.9 if successfully checked out with correct pizza (d2, large)
    - 0.6 if correct item is in cart (not yet checked out)
    - 0.4 if correct item is selected
    - 0.2 if on dominos platform
    - 0.1 baseline partial credit
    """
    # Successful checkout with correct item
    if env_instance.status == "success":
        for item in env_instance.cart:
            if item["product"]["id"] == "d2" and item["variant"] == "large":
                return 0.9
        return 0.4

    # Correct item in cart
    for item in env_instance.cart:
        if item["product"]["id"] == "d2" and item["variant"] == "large":
            return 0.6

    # Correct item selected
    if env_instance.selected_product:
        if env_instance.selected_product["product"]["id"] == "d2" and env_instance.selected_product["variant"] == "large":
            return 0.4

    # At least on the right platform
    if env_instance.current_platform == "dominos":
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
        "description": "Buy a 20W iPhone 15 charger.",
        "grader": grade_task_medium
    },
    {
        "id": "task_3_hard",
        "description": "Order a large Pepperoni pizza and checkout.",
        "grader": grade_task_hard
    }
]
