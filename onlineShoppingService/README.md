# 🛒 Online Shopping Service

A comprehensive online shopping service implementation demonstrating various design patterns and software engineering principles. This project showcases a real-world e-commerce application with clean architecture, proper separation of concerns, and extensive use of design patterns.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Design Patterns](#design-patterns)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Design Pattern Explanations](#design-pattern-explanations)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Online Shopping Service is a complete e-commerce platform that enables users to browse products, manage shopping carts, place orders, and process payments. Built with clean architecture principles, it showcases multiple design patterns working together to create a maintainable, extensible, and scalable system.

### Key Highlights

- **User Management**: Registration, authentication, and profile management
- **Product Catalog**: Product management with inventory tracking
- **Shopping Cart**: Add, remove, and update items in cart
- **Order Management**: Complete order lifecycle with state management
- **Payment Processing**: Multiple payment methods support
- **Search Functionality**: Flexible search strategies
- **Inventory Management**: Real-time stock tracking with observer notifications
- **Concurrent Access**: Thread-safe operations for high-traffic scenarios

## ✨ Features

### Core Functionality

- **User Management**: User registration, login, authentication, and profile management
- **Product Management**: Product catalog with categories, pricing, and descriptions
- **Inventory Management**: Real-time stock tracking with automatic notifications
- **Shopping Cart**: Add, remove, update items with quantity management
- **Order Processing**: Complete order workflow from cart to delivery
- **Payment Processing**: Multiple payment methods (Credit Card, Debit Card, UPI, Cash on Delivery)
- **Search & Discovery**: Flexible search by name, category, or price range
- **Order State Management**: Order lifecycle with proper state transitions
- **Observer Notifications**: Real-time updates for inventory and order status

### Advanced Features

- **Product Decorators**: Gift wrapping and other product enhancements
- **Concurrent Operations**: Thread-safe inventory and order management
- **State Management**: Order state transitions (Pending → Placed → Shipped → Delivered/Cancelled)
- **Strategy Pattern**: Flexible payment and search strategies
- **Error Handling**: Comprehensive exception handling for edge cases
- **Observer Pattern**: Real-time notifications for inventory and order updates

## 🏗️ Design Patterns

This project demonstrates the following design patterns:

### 1. **Singleton Pattern**

- **Implementation**: `OnlineShoppingServiceSystem`
- **Purpose**: Ensures only one instance of the shopping service exists
- **Benefits**: Centralized state management, resource optimization

### 2. **Observer Pattern**

- **Implementation**: Inventory and order status notifications
- **Components**: `InventorySubject`, `InventoryObserver`, `OrderSubject`, `OrderObserver`
- **Benefits**: Loose coupling, real-time notifications

### 3. **Strategy Pattern**

- **Implementation**: Payment methods and search strategies
- **Components**: `PaymentStrategy`, `SearchStrategy`
- **Benefits**: Easy addition of new payment methods and search algorithms

### 4. **State Pattern**

- **Implementation**: Order state management
- **Components**: `OrderState`, `PendingState`, `PlacedState`, `ShippedState`, `DeliveredState`, `CancelledState`
- **Benefits**: Clean state transitions, behavior encapsulation

### 5. **Decorator Pattern**

- **Implementation**: Product enhancements (gift wrapping)
- **Components**: `ProductDecorator`, `GiftWrapperDecorator`
- **Benefits**: Dynamic behavior addition without modifying base classes

### 6. **Facade Pattern**

- **Implementation**: `OnlineShoppingServiceSystem` as a simplified interface
- **Benefits**: Simplified client interface, subsystem complexity hiding

### 7. **Repository Pattern**

- **Implementation**: Service layer abstracts data access
- **Benefits**: Clean data access layer, separation of concerns

## 📁 Project Structure

```
onlineShoppingService/
├── app/
│   ├── models/
│   │   ├── observers/
│   │   │   ├── inventory_observer.py      # Observer pattern for inventory
│   │   │   └── order_observer.py          # Observer pattern for orders
│   │   ├── account.py                     # User account with cart and order history
│   │   ├── address.py                     # Shipping address model
│   │   ├── cart_item.py                   # Shopping cart item
│   │   ├── enums.py                       # Enumerations and constants
│   │   ├── exceptions.py                  # Custom exceptions
│   │   ├── order.py                       # Order model with state pattern
│   │   ├── order_item.py                  # Order item model
│   │   ├── order_states.py                # State pattern implementation
│   │   ├── payment_strategy.py            # Payment strategy pattern
│   │   ├── product.py                     # Product model
│   │   ├── product_decorator.py           # Decorator pattern for products
│   │   ├── search_strategy.py             # Search strategy pattern
│   │   ├── shopping_cart.py               # Shopping cart model
│   │   └── user.py                        # User model with observers
│   ├── services/
│   │   ├── inventory_service.py          # Inventory management service
│   │   ├── order_service.py               # Order management service
│   │   ├── payment_service.py             # Payment processing service
│   │   ├── search_service.py              # Search functionality service
│   │   └── user_service.py                # User management service
├── online_shopping_service_system.py      # Main service (Singleton + Facade)
└── run.py                                  # Demo script
```

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (for concurrent operations)
- **Dependencies**: Only Python standard library (no external dependencies)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd onlineShoppingService

# Or download and extract the project folder
```

### 2. Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Verify Installation

```bash
python --version  # Should be 3.8+
```

## 🎯 Usage

### Quick Start

```bash
# Run the demo
python run.py
```

### Basic Usage Examples

#### 1. Create and Run the Service

```python
from online_shopping_service_system import OnlineShoppingServiceSystem
from app.models.user import User
from app.models.product import Product
from app.models.address import Address
from app.models.enums import UserType, ProductCategory

# Get service instance (Singleton)
system = OnlineShoppingServiceSystem.get_instance()

# Create and register users
address = Address("123 Main St", "New York", "NY", "10001", "USA")
user = User("alice123", "password123", address, UserType.NORMAL_USER)
system.register_user(user)

# Add products to inventory
laptop = Product("Dell XPS 15", 1499.99, "High-performance laptop", ProductCategory.ELECTRONICS)
system.inventory_service.add_product(laptop, 10)
```

#### 2. Add Items to Cart and Place Order

```python
from app.models.payment_strategy import CreditCardPaymentStrategy

# Add product to cart
system.add_product_to_cart(user, laptop, 1)

# Place order with payment
payment_strategy = CreditCardPaymentStrategy("1234-5678-9012-3456", "123", "12/25")
order = system.place_order(user, payment_strategy)
```

#### 3. Search Products

```python
from app.models.search_strategy import SearchByNameStrategy, SearchByCategoryStrategy

# Search by name
name_strategy = SearchByNameStrategy()
results = system.search_products(name_strategy, "laptop")

# Search by category
category_strategy = SearchByCategoryStrategy()
results = system.search_products(category_strategy, ProductCategory.ELECTRONICS)
```

## 📚 API Reference

### Core Service Methods

#### User Management

```python
# Register user
system.register_user(user: User) -> None

# Login user
system.login_user(user_name: str, password: str) -> None

# Get user
system.user_service.get_user(user_id: str) -> User
```

#### Product Management

```python
# Add product to inventory
system.inventory_service.add_product(product: Product, quantity: int) -> None

# Get product stock
system.inventory_service.get_product_stock_count(product_id: str) -> int

# Check product availability
system.inventory_service.is_product_available(product_id: str) -> bool
```

#### Shopping Cart Operations

```python
# Add product to cart
system.add_product_to_cart(user: User, product: Product, quantity: int) -> None

# Remove product from cart
system.remove_product_from_cart(user: User, product: Product) -> None

# Update product quantity in cart
system.update_product_in_cart(user: User, product: Product, quantity: int) -> None
```

#### Order Operations

```python
# Place order
system.place_order(user: User, payment_strategy: PaymentStrategy) -> Optional[Order]

# Get order history
user.get_account().get_order_history() -> list[Order]
```

#### Search Operations

```python
# Search products
system.search_products(search_strategy: SearchStrategy, keyword: Any) -> list[Product]
```

### Data Models

#### User

```python
class User:
    def __init__(self, user_name: str, password: str, shipping_address: Address, user_type: UserType)
    def get_user_id(self) -> str
    def get_user_name(self) -> str
    def get_account(self) -> Account
```

#### Product

```python
class Product:
    def __init__(self, name: str, price: float, description: str, category: ProductCategory)
    def get_product_id(self) -> str
    def get_name(self) -> str
    def get_price(self) -> float
    def is_available(self) -> bool
```

#### Order

```python
class Order:
    def __init__(self, user: User)
    def get_order_id(self) -> str
    def get_status(self) -> OrderStatus
    def get_total_price(self) -> float
    def add_order_item(self, order_item: OrderItem) -> None
```

## 🎨 Design Pattern Explanations

### 1. Singleton Pattern

```python
class OnlineShoppingServiceSystem:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Why**: Ensures single point of control for the shopping system, prevents multiple instances that could lead to data inconsistency.

### 2. Observer Pattern

```python
# Inventory changes notify all subscribed users
product.add_observer(user1)
product.add_observer(admin)
product.set_status(ProductStatus.OUT_OF_STOCK)  # All observers get notified
```

**Why**: Loose coupling between inventory changes and user notifications. Easy to add/remove subscribers without modifying the product class.

### 3. Strategy Pattern

```python
# Different payment methods
credit_card = CreditCardPaymentStrategy("1234-5678", "123", "12/25")
upi = UpiPaymentStrategy("user@paytm")
cash = CashOnDeliveryPaymentStrategy()

# Same interface, different implementations
payment_result = strategy.pay(amount)
```

**Why**: Easy to add new payment methods without modifying existing code. Each payment method encapsulates its own logic.

### 4. State Pattern

```python
# Order states
pending_state = PendingState()
placed_state = PlacedState()
shipped_state = ShippedState()

# State transitions
order.state = pending_state
order.place_order()  # Transitions to placed_state
```

**Why**: Clean separation of behavior based on state. Easy to add new states and transitions.

### 5. Decorator Pattern

```python
# Product decorators
base_product = Product("Book", 29.99, "A book", ProductCategory.BOOKS)
gift_wrapped = GiftWrapperDecorator(base_product)
# Gift wrapped product has additional cost and description
```

**Why**: Add features to products dynamically without modifying the base Product class.

## 🧪 Testing

### Run the Demo

```bash
python run.py
```

### Test Individual Components

```python
# Test user creation
from app.models.user import User
from app.models.address import Address
from app.models.enums import UserType

address = Address("123 Main St", "New York", "NY", "10001", "USA")
user = User("test_user", "password", address, UserType.NORMAL_USER)
assert user.get_user_name() == "test_user"

# Test product creation
from app.models.product import Product
from app.models.enums import ProductCategory

product = Product("Test Product", 99.99, "Test description", ProductCategory.ELECTRONICS)
assert product.get_name() == "Test Product"
```

### Expected Demo Output

The demo should show:

- User registration and authentication
- Product management and inventory tracking
- Shopping cart operations
- Order placement with different payment methods
- Search functionality with different strategies
- Observer pattern notifications
- Order state transitions
- Error handling scenarios
- System summary

## 🔧 Configuration

### Payment Strategies

```python
# Modify in app/models/payment_strategy.py
class CustomPaymentStrategy(PaymentStrategy):
    def pay(self, amount: float) -> PaymentResult:
        # Custom payment logic
        return PaymentResult(amount, PaymentStatus.SUCCESS, "Payment successful")
```

### Search Strategies

```python
# Modify in app/models/search_strategy.py
class CustomSearchStrategy(SearchStrategy):
    def search(self, keyword: Any) -> list[Product]:
        # Custom search logic
        return filtered_products
```

### Order States

```python
# Modify in app/models/order_states.py
class CustomOrderState(OrderState):
    def place_order(self, order: Order) -> bool:
        # Custom state behavior
        return True
```

## 🚀 Extending the System

### Adding New Payment Methods

```python
class PayPalPaymentStrategy(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> PaymentResult:
        # PayPal payment logic
        return PaymentResult(amount, PaymentStatus.SUCCESS, "PayPal payment successful")
```

### Adding New Search Strategies

```python
class SearchByRatingStrategy(SearchStrategy):
    def search(self, min_rating: float) -> list[Product]:
        return [product for product in self.products if product.get_rating() >= min_rating]
```

### Adding New Product Decorators

```python
class ExpressShippingDecorator(ProductDecorator):
    def get_price(self) -> float:
        return self.product.get_price() + 10.0  # Add express shipping fee

    def get_description(self) -> str:
        return f"{self.product.get_description()} (Express Shipping)"
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

```
ModuleNotFoundError: No module named 'app'
```

**Solution**: Ensure you're running from the correct directory and Python path is set correctly.

#### 2. Circular Import Issues

```
ImportError: cannot import name 'Product' from partially initialized module
```

**Solution**: Use `TYPE_CHECKING` and forward references for type hints.

#### 3. Inventory Issues

```
OutOfStockException: Product not available
```

**Solution**: Check product stock before adding to cart or placing order.

## 📈 Performance Considerations

### Memory Usage

- **Users**: ~2KB per user
- **Products**: ~500B per product
- **Orders**: ~3KB per order
- **Cart Items**: ~200B per item

### Concurrent Operations

- Thread-safe inventory management
- Atomic order operations
- Observer pattern for efficient notifications

### Scalability

- Singleton pattern for centralized state
- Service layer for business logic separation
- Observer pattern for loose coupling

## 🤝 Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write descriptive docstrings
- Keep methods focused and small

### Adding Features

1. Create feature branch
2. Implement with tests
3. Update documentation
4. Submit pull request

### Reporting Issues

- Use descriptive issue titles
- Include steps to reproduce
- Provide system information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Design patterns inspired by Gang of Four
- Clean architecture principles
- Python best practices
- Real-world e-commerce system requirements

## 📞 Support

For questions or support:

- Create an issue in the repository
- Check the troubleshooting section
- Review the demo output for examples

---

**Happy Shopping! 🛒**
