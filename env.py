import json
import os

class ShoppingEnv:
    def __init__(self, dataset_path="dataset.json"):
        with open(dataset_path, "r") as f:
            self.catalog = json.load(f)
        
        self.available_platforms = list(self.catalog.keys())
        self.reset("empty")

    def reset(self, user_request, budget=100000):
        self.user_request = user_request
        self.budget = budget
        self.cart = []
        self.current_platform = None
        self.search_results = []
        self.selected_product = None
        self.status = "active" # active, success, failed
        
        return self.state()

    def state(self):
        return {
            "user_request": self.user_request,
            "available_platforms": self.available_platforms,
            "current_platform": self.current_platform,
            "budget": self.budget,
            "cart": self.cart,
            "search_results": self.search_results,
            "selected_product": self.selected_product,
            "status": self.status
        }

    def step(self, action):
        action_type = action.get("type")
        
        if self.status != "active":
            return self.state(), -1, True, "Environment already terminated"

        reward = -0.01  # Base penalty per step to encourage efficiency
        done = False
        message = ""

        try:
            if action_type == "choose_platform":
                platform = action.get("platform")
                if platform in self.available_platforms:
                    self.current_platform = platform
                    message = f"Platform switched to {platform}"
                    reward += 0.1
                else:
                    self.status = "failed"
                    done = True
                    message = "Invalid platform selected"
                    reward -= 0.5  # Heavy penalty for destructive/invalid action

            elif action_type == "search_product":
                if not self.current_platform:
                    message = "Must choose platform first"
                    reward -= 0.1
                else:
                    query = action.get("query", "").lower()
                    platform_data = self.catalog[self.current_platform]["products"]
                    query_words = query.split()
                    self.search_results = []
                    for p in platform_data:
                        name_and_cat = (p["name"] + " " + p["category"]).lower()
                        if any(word in name_and_cat for word in query_words) or query in name_and_cat:
                            self.search_results.append(p)
                    message = f"Found {len(self.search_results)} products"
                    if len(self.search_results) > 0:
                        reward += 0.1

            elif action_type == "select_product":
                product_id = action.get("product_id")
                variant = action.get("variant")
                
                # Check within search results or platform catalog
                all_products = self.catalog[self.current_platform]["products"] if self.current_platform else []
                product = next((p for p in all_products if p["id"] == product_id), None)
                
                if product:
                    if variant in product["variants"]:
                        self.selected_product = {"product": product, "variant": variant}
                        message = f"Selected {product['name']} ({variant})"
                        reward += 0.2
                    else:
                        message = f"Invalid variant. Available: {product['variants']}"
                        reward -= 0.1
                else:
                    message = "Product ID not found"
                    reward -= 0.1

            elif action_type == "add_to_cart":
                if self.selected_product:
                    price = self.selected_product["product"]["price"]
                    if self.budget >= price:
                        self.cart.append(self.selected_product)
                        self.budget -= price
                        self.selected_product = None
                        message = "Added to cart"
                        reward += 0.5
                    else:
                        message = "Insufficient budget"
                        reward -= 0.1
                else:
                    message = "No product selected"
                    reward -= 0.1

            elif action_type == "checkout":
                if len(self.cart) > 0:
                    self.status = "success"
                    done = True
                    message = "Checkout successful"
                    # We defer final task completion reward to the grader, but give a small positive signal here
                    reward += 1.0 
                else:
                    self.status = "failed"
                    done = True
                    message = "Cart is empty, checkout failed"
                    reward -= 0.5

            else:
                self.status = "failed"
                done = True
                message = f"Invalid action: {action_type}"
                reward -= 0.5  # Penalty for invalid action to discourage hallucinations

        except Exception as e:
            self.status = "failed"
            done = True
            message = f"Error: {e}"
            reward -= 0.5

        # Strictly clamp reward to 0.0-1.0 range to satisfy evaluation bounds
        reward = max(0.0, min(1.0, reward))

        return self.state(), reward, done, message
