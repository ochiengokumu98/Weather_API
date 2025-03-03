from time import process_time
print(process_time())

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}
profit=0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}
total_coins=0
# profit=0
#TODO print the report of the coffee machine.

def is_resources_enough(order_ingredients):
    """Returns True when order can be made and False when there is no enough resources."""
    for items in order_ingredients:
        if order_ingredients[items] >= resources[items]:
            print(f"Sorry there is not enough water.{items}")
            return False
    return True

def coin_process():
    global total_coins
    """Returns the total of the coins the customer inserts."""
    print("Please insert coins.")
    quarters = int(input("How many quarters? "))  # Each quarter = 0.25
    dimes = int(input("How many dimes? "))  # Each dime = 0.10
    nickels = int(input("How many nickels? "))  # Each nickel = 0.05
    pennies = int(input("How many pennies? "))  # Each penny = 0.01

    total_coins = quarters * 0.25 + dimes * 0.10 + nickels * 0.05 + pennies * 0.01
    return total_coins

def is_successful_transaction(money_received, drink_cost):
    """returns True when the payment is accepted or False when the transaction is denied i.e.
    when the money paid is insufficient."""
    if money_received>=drink_cost:
        change=round(money_received-drink_cost, 2)
        print(f"Here is ${change} in change")
        global profit
        profit+=drink_cost
        return True
    else:
        print(f"Sorry, that's not enough money. Your money ${total_coins:.2f} is refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    """deduct the required ingredients from the resources"""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
        print(f"Here is your {drink_name}☕")

machine_on = True

while machine_on:

     try:
            customer_choice = input("What would you like? (espresso/latte/cappuccino/report): ").lower()

            if customer_choice == "off":
                machine_on = False
                print("Thank you. Welcome soon.")

            elif customer_choice == "report":
                print(f"Water: {resources['water']}ml")
                print(f"Milk: {resources['milk']}ml")
                print(f"Coffee: {resources['coffee']}gms")
                print(f"Money: {profit}$")

            elif customer_choice in MENU:
                drink = MENU[customer_choice]
                for key, value in drink.items():
                    if isinstance(value, dict):  # Check if value is another dictionary
                        print(f"{key}:")
                        for sub_key, sub_value in value.items():
                            print(f"  {sub_key}: {sub_value}")
                    else:
                        print(f"{key}: {value}")
                if is_resources_enough(drink["ingredients"]):
                    payment = coin_process()
                    if is_successful_transaction(payment, drink["cost"]):
                        make_coffee(customer_choice, drink["ingredients"])

            else:
                raise ValueError("Invalid choice! Please select from the menu.")  # Affects only the menu

     except ValueError as e:
         print(e)



