# Coffee Vending Machine System – UML, Design Patterns, and Data Flow

---

## 1. UML Class Diagram (Textual / Interview-Friendly)

```
+----------------------+        uses       +----------------------+
|   VendingMachine     |------------------>|  VendingMachineState |
|----------------------|                   |    (Abstract)        |
| - selected_coffee    |                   |----------------------|
| - inserted_coins[]   |                   | + insert_coin()      |
| - current_coffee     |                   | + select_coffee()    |
| - coffee_decorators[]|                   | + dispense_coffee()  |
| - state              |                   | + return_change()    |
|----------------------|                   | + cancel()           |
| + insert_coin()      |                   +--------+-------------+
| + select_coffee()    |                            |
| + dispense_coffee()  |                            | implements
| + return_change()    |                            |
| + cancel()           |                            v
| + create_coffee()    |        +-----------------------------------+
+--------+-------------+        |      State Implementations        |
         |                      +-----------------------------------+
         | uses                 | ReadyState                        |
         |                      | CashCollectedState                |
         |                      | DispenseItemState                 |
         |                      | DispenseChangeState               |
         |                      | TransactionCancelledState         |
         |                      +-----------------------------------+
         v
+----------------------+        +----------------------+
|   CoffeeFactory      |------->|      Coffee          |
|----------------------|        |----------------------|
| + create_coffee()    |        | - type               |
+----------------------+        | - recipe[]           |
                                | - price              |
                                |----------------------|
                                | + grind_beans()      |
                                | + brew()             |
                                | + add_condiments()   |
                                | + pour_into_cup()    |
                                | + prepare()          |
                                | + get_price()        |
                                | + get_recipe()       |
                                +--------+-------------+
                                         |
                                         | extends
                                         v
                    +-----------+--------+--------+
                    |           |                 |
            +-------+----+ +----+----+    +-------+----+
            | Espresso   | | Latte   |    | Cappuccino |
            +------------+ +---------+    +------------+

+----------------------+        +----------------------+
|  CoffeeDecorator     |------->|      Coffee          |
|  (Abstract)          |        |----------------------|
|----------------------|        | + get_price()        |
| - coffee             |        +----------------------+
|----------------------|                  ^
| + get_price()        |                  |
| + get_recipe()       |                  | wraps
+--------+-------------+                  |
         |                                |
         | extends                        |
         v                                |
+--------+--------+--------+              |
| SugarDecorator  |        |              |
| ExtraMilkDecorator       |              |
| CaramelDecorator         |              |
+-----------------+--------+--------------+

+----------------------+        +----------------------+
|    Inventory         |<-------|  InventorySubject    |
|  (Singleton)         |        |----------------------|
|----------------------|        | - observers[]        |
| - ingredients{}      |        |----------------------|
| - threshold_quantity |        | + add_observer()     |
|----------------------|        | + remove_observer()  |
| + add_item()         |        | + notify_observers() |
| + remove_item()       |       +----------------------+
| + check_availability()|                 ^
| + consume_ingredients()|                |
+--------+-------------+                  |
         |                                | implements
         | notifies                       |
         v                                |
+----------------------+                  |
|   InventoryObserver  |<----------------+
|  (Abstract)          |
|----------------------|
| + update_inventory() |
+--------+-------------+
         |
         | implements
         v
+----------------------+
|       Admin          |
|----------------------|
| - admin_id           |
| - name               |
|----------------------|
| + update_inventory() |
| + add_item()         |
| + remove_item()      |
+----------------------+

+----------------------+        +----------------------+
| TransactionService   |------->| PaymentProcessor     |
|----------------------|        |----------------------|
| + validate_payment() |        | + process_payment()  |
| + calculate_change() |        | + calculate_change() |
+----------------------+        +----------------------+
```

---

## 2. Design Patterns Used

### **State Pattern** - Vending Machine States

- Encapsulates state-specific behavior for the vending machine
- States: `ReadyState`, `CashCollectedState`, `DispenseItemState`, `DispenseChangeState`, `TransactionCancelledState`
- Each state defines valid operations and transitions
- Eliminates complex if-else chains for state management

### **Singleton Pattern** - Inventory

- Ensures only one instance of Inventory exists across the application
- Thread-safe implementation with double-checked locking
- Shared inventory across all vending machine instances

### **Observer Pattern** - Inventory Notifications

- `Inventory` (Subject) notifies `Admin` (Observers) when ingredients drop below threshold
- Decouples inventory management from admin notification logic
- Supports multiple admins receiving notifications

### **Factory Pattern** - Coffee Creation

- `CoffeeFactory` creates coffee instances based on `CoffeeType`
- Encapsulates object creation logic
- Easy to extend with new coffee types

### **Decorator Pattern** - Coffee Customization

- `CoffeeDecorator` wraps base `Coffee` to add features (sugar, extra milk, caramel)
- Allows dynamic addition of features at runtime
- Maintains single responsibility principle

### **Template Method Pattern** - Coffee Preparation

- `Coffee.prepare()` defines the algorithm skeleton
- Subclasses (Espresso, Latte, Cappuccino) implement specific steps
- Consistent preparation flow across all coffee types

---

## 3. State Machine Flow

### State Transitions

```
┌─────────┐
│  Ready  │ (Initial State)
└────┬────┘
     | insert_coin()
     v
┌──────────────┐
│CashCollected │
└──────┬───────┘
       | select_coffee_type()
       | (validates payment & inventory)
       v
┌──────────────┐
│DispenseItem  │
└──────┬───────┘
       | dispense_coffee()
       | (prepares & dispenses)
       v
       ├─── change > 0 ───> ┌──────────────┐
       |                    │DispenseChange│
       |                    └──────┬───────┘
       |                           | return_change()
       |                           v
       |                    ┌─────────┐
       |                    │  Ready  │
       |                    └─────────┘
       |
       └─── change == 0 ───> ┌─────────┐
                             │  Ready  │
                             └─────────┘

┌──────────────┐
│CashCollected │
└──────┬───────┘
       | cancel()
       v
┌──────────────────────┐
│TransactionCancelled  │
└──────┬───────────────┘
       | (returns coins)
       v
┌─────────┐
│  Ready  │
└─────────┘
```

### State Responsibilities

1. **ReadyState**: Machine ready to accept cash

   - Valid: `insert_coin()`
   - Invalid: All other operations

2. **CashCollectedState**: Cash collected, waiting for selection

   - Valid: `insert_coin()`, `select_coffee_type()`, `cancel()`
   - Invalid: `dispense_coffee()`, `return_change()`

3. **DispenseItemState**: Dispensing coffee

   - Valid: `dispense_coffee()` (auto-called)
   - Invalid: All other operations

4. **DispenseChangeState**: Returning change

   - Valid: `return_change()` (auto-called)
   - Invalid: All other operations

5. **TransactionCancelledState**: Transaction cancelled
   - Valid: `return_change()`, `cancel()` (both transition to Ready)
   - Invalid: All other operations

---

## 4. Class Structure

### VendingMachine

```python
class VendingMachine:
    def __init__(self):
        self.selected_coffee_type: CoffeeType | None = None
        self.inserted_coins: list[Coin] = []
        self.current_coffee = None
        self.coffee_decorators: list = []
        self.state: VendingMachineState = ReadyState(self)

    def insert_coin(self, coin: Coin) -> None:
        self.state.insert_coin(coin)

    def select_coffee_type(self, coffee_type: CoffeeType) -> None:
        self.state.select_coffee_type(coffee_type)

    def create_coffee_with_decorators(self, coffee_type: CoffeeType):
        coffee = CoffeeFactory.create_coffee(coffee_type)
        if self.coffee_decorators:
            for decorator_class in self.coffee_decorators:
                coffee = decorator_class(coffee)
        return coffee
```

### Coffee (Template Method)

```python
class Coffee:
    def prepare(self):
        self.grind_beans()
        self.brew()
        self.add_condiments()
        self.pour_into_cup()

    def brew(self):
        raise NotImplementedError

    def add_condiments(self):
        pass
```

### Inventory (Singleton + Observer Subject)

```python
class Inventory(InventorySubject):
    _instance: Optional["Inventory"] = None

    def __init__(self):
        self.ingredients: dict[str, Ingredient] = {}
        self.threshold_quantity = 2

    def remove_item(self, item: str, quantity: int) -> None:
        ingredient.update_quantity(-quantity)
        if ingredient.get_quantity() <= self.threshold_quantity:
            self.notify_observers(ingredient.get_name(), ingredient.get_quantity())
```

### Admin (Observer)

```python
class Admin(InventoryObserver):
    def update_inventory_status(self, item: str, quantity: int) -> None:
        print(f"Admin {self.name} received update about {item} which is now {quantity}")
```

---

## 5. Data Flow (End-to-End)

### Coffee Order Flow

```
User Action
    |
    | insert_coin(Coin.HUNDRED)
    v
+------------------+
|   ReadyState     |  (State Pattern)
+------------------+
    |
    | Transition to CashCollectedState
    v
+------------------+
| CashCollectedState|
+------------------+
    |
    | select_coffee_type(LATTE)
    |  1. Create coffee with decorators (Factory + Decorator)
    |  2. Validate payment (TransactionService)
    |  3. Check inventory availability
    |  4. Transition to DispenseItemState
    v
+------------------+
| DispenseItemState|
+------------------+
    |
    | dispense_coffee() (auto-called)
    |  1. Consume ingredients from Inventory
    |  2. Prepare coffee (Template Method)
    |  3. Calculate change
    |  4. If change > 0: Transition to DispenseChangeState
    |     Else: Transition to ReadyState
    v
+------------------+
| DispenseChangeState| (if change > 0)
+------------------+
    |
    | return_change() (auto-called)
    | Transition to ReadyState
    v
+------------------+
|   ReadyState     |
+------------------+
```

### Inventory Notification Flow

```
Coffee Order
    |
    | consume_ingredients()
    v
+------------------+
|    Inventory     |  (Singleton)
+------------------+
    |
    | remove_item() checks threshold
    | if quantity <= threshold_quantity:
    v
+------------------+
| notify_observers() |
+------------------+
    |
    | For each observer
    v
+------------------+
|      Admin       |  (Observer Pattern)
+------------------+
    |
    | update_inventory_status()
    | Print notification
```

---

## 6. Key Features

### **State Management**

- ✅ Clean state transitions with State Pattern
- ✅ Invalid operation handling with clear error messages
- ✅ Automatic state progression (no manual dispense/change calls needed)

### **Payment Processing**

- ✅ Payment validation before dispensing
- ✅ Automatic change calculation and return
- ✅ Support for multiple coin denominations

### **Inventory Management**

- ✅ Singleton inventory shared across all machines
- ✅ Thread-safe operations with locks
- ✅ Low inventory notifications via Observer Pattern
- ✅ Ingredient availability checks before dispensing

### **Coffee Customization**

- ✅ Decorator Pattern for adding extras (sugar, milk, caramel)
- ✅ Dynamic price calculation with decorators
- ✅ Factory Pattern for coffee creation

### **Error Handling**

- ✅ Insufficient payment detection
- ✅ Out of stock ingredient handling
- ✅ Invalid state operation prevention

---

## 7. Usage Examples

### Basic Coffee Order

```python
from app.models.vending_machine import VendingMachine
from app.models.enums import CoffeeType, Coin

machine = VendingMachine()

# Insert coins
machine.insert_coin(Coin.HUNDRED)

# Select coffee (automatically dispenses and returns change if needed)
machine.select_coffee_type(CoffeeType.LATTE)
```

### Coffee with Decorators

```python
from app.decorators.coffee_decorator import SugarDecorator, ExtraMilkDecorator

machine = VendingMachine()
machine.coffee_decorators = [SugarDecorator, ExtraMilkDecorator]

machine.insert_coin(Coin.HUNDRED)
machine.insert_coin(Coin.HUNDRED)  # Extra for decorators
machine.select_coffee_type(CoffeeType.LATTE)
```

### Observer Pattern - Admin Notifications

```python
from app.models.inventory import Inventory
from app.models.admin import Admin

inventory = Inventory.get_instance()

admin1 = Admin("Rajesh Kumar")
admin2 = Admin("Priya Sharma")

inventory.add_observer(admin1)
inventory.add_observer(admin2)

# When ingredients drop below threshold (2), admins are notified
# Admin Rajesh Kumar received update about inventory status of MILK which is now 2
# Admin Priya Sharma received update about inventory status of MILK which is now 2
```

### Transaction Cancellation

```python
machine = VendingMachine()
machine.insert_coin(Coin.HUNDRED)
machine.cancel()  # Returns coins and transitions to TransactionCancelledState
```

---

## 8. Design Principles Applied

### **SOLID Principles**

- ✅ **Single Responsibility**: Each state handles only its specific behavior
- ✅ **Open/Closed**: Easy to add new states or coffee types without modifying existing code
- ✅ **Liskov Substitution**: All states are substitutable through base `VendingMachineState`
- ✅ **Interface Segregation**: Clean interfaces with only necessary methods
- ✅ **Dependency Inversion**: States depend on abstractions (VendingMachine, TransactionService)

### **Other Principles**

- ✅ **DRY (Don't Repeat Yourself)**: Shared logic in base classes and services
- ✅ **KISS (Keep It Simple)**: Clear state transitions and responsibilities
- ✅ **Separation of Concerns**: Business logic in services, state management in states

---

## 9. Extension Points

### Adding New Coffee Type

1. Add to `CoffeeType` enum
2. Create new class extending `Coffee`
3. Implement `brew()` method
4. Add to `CoffeeFactory`

```python
class Americano(Coffee):
    def __init__(self):
        super().__init__(CoffeeType.AMERICANO)
        self.recipe = [Ingredient(IngredientType.COFFEE_BEANS.value, 10),
                      Ingredient(IngredientType.WATER.value, 50)]
        self.price = 60

    def brew(self):
        print("Brewing Americano with hot water")
```

### Adding New State

1. Extend `VendingMachineState`
2. Implement all abstract methods
3. Define state transitions

```python
class MaintenanceState(VendingMachineState):
    def insert_coin(self, coin: Coin) -> None:
        print("Invalid: Machine is under maintenance")
    # ... implement other methods
```

### Adding New Decorator

1. Extend `CoffeeDecorator`
2. Override `get_price()` and optionally `get_recipe()`

```python
class WhippedCreamDecorator(CoffeeDecorator):
    def get_price(self) -> float:
        return self.coffee.get_price() + 15
```

### Adding New Observer

1. Implement `InventoryObserver`
2. Register with Inventory

```python
class InventoryAlert(InventoryObserver):
    def update_inventory_status(self, item: str, quantity: int) -> None:
        # Send email/SMS alert
        pass
```

---

## 10. Why This Design Works Well in Interviews

### **Design Patterns Applied:**

- ✅ **State Pattern**: Clean state management
- ✅ **Singleton Pattern**: Shared inventory
- ✅ **Observer Pattern**: Admin notifications
- ✅ **Factory Pattern**: Coffee creation
- ✅ **Decorator Pattern**: Coffee customization
- ✅ **Template Method Pattern**: Coffee preparation

### **Key Features:**

- ✅ **Thread-Safe**: Lock-based synchronization in Inventory
- ✅ **Extensible**: Easy to add new states, coffee types, decorators
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Production-Ready**: Error handling, validation, notifications

### **Real-World Scenarios:**

- Similar to actual vending machine systems
- Handles edge cases (insufficient payment, out of stock, cancellation)
- Supports concurrent operations (multiple machines, shared inventory)

---

## 11. Sample Runtime Example

### Complete Flow

```python
from app.models.vending_machine import VendingMachine
from app.models.enums import CoffeeType, Coin
from app.decorators.coffee_decorator import SugarDecorator

# Setup inventory
from app.models.inventory import Inventory
from app.models.enums import IngredientType
inventory = Inventory.get_instance()
inventory.add_item(IngredientType.COFFEE_BEANS.value, 100)
inventory.add_item(IngredientType.MILK.value, 50)
inventory.add_item(IngredientType.WATER.value, 200)

# Order coffee
machine = VendingMachine()
machine.coffee_decorators = [SugarDecorator]
machine.insert_coin(Coin.HUNDRED)
machine.select_coffee_type(CoffeeType.LATTE)

# Output:
# Grinding beans for LATTE
# Brewing Latte with hot water and coffee beans
# Adding milk to Latte
# Adding foam to Latte
# Pouring Coffee of type LATTE into a cup
# Returning change: 20 INR
```

---

## 12. State Transition Table

| Current State        | Operation            | Valid? | Next State             |
| -------------------- | -------------------- | ------ | ---------------------- |
| Ready                | insert_coin()        | ✅     | CashCollected          |
| Ready                | select_coffee_type() | ❌     | Ready                  |
| CashCollected        | insert_coin()        | ✅     | CashCollected          |
| CashCollected        | select_coffee_type() | ✅     | DispenseItem           |
| CashCollected        | cancel()             | ✅     | TransactionCancelled   |
| DispenseItem         | dispense_coffee()    | ✅     | DispenseChange / Ready |
| DispenseChange       | return_change()      | ✅     | Ready                  |
| TransactionCancelled | return_change()      | ✅     | Ready                  |

---

If you want next:

- **Sequence diagrams** for detailed interaction flow
- **Concurrency handling** for multiple simultaneous orders
- **Payment gateway integration** for card payments
- **Analytics and reporting** for sales tracking

Tell me which one you want.
