from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant, Cuisine, RestaurantCuisine, MenuItem, RestaurantHours
from accounts.models import UserProfile
import random
from datetime import time

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for development'

    def handle(self, *args, **options):
        # Create sample users
        if not User.objects.filter(email='admin@example.com').exists():
            admin_user = User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='admin123',
                phone_number='+1234567890'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create sample restaurant owners
        owners = []
        for i in range(5):
            email = f'owner{i}@example.com'
            if not User.objects.filter(email=email).exists():
                owner = User.objects.create_user(
                    email=email,
                    username=f'owner{i}',
                    password='owner123',
                    phone_number=f'+123456789{i}',
                    is_restaurant_owner=True
                )
                owners.append(owner)
                self.stdout.write(self.style.SUCCESS(f'Created owner {owner.email}'))
        
        # Create sample customers
        customers = []
        for i in range(10):
            email = f'customer{i}@example.com'
            if not User.objects.filter(email=email).exists():
                customer = User.objects.create_user(
                    email=email,
                    username=f'customer{i}',
                    password='customer123',
                    phone_number=f'+123456788{i}'
                )
                customers.append(customer)
                self.stdout.write(self.style.SUCCESS(f'Created customer {customer.email}'))
        
        # Create sample cuisines
        cuisine_names = ['Italian', 'Chinese', 'Mexican', 'Indian', 'Japanese', 'Thai', 'French', 'American']
        cuisines = []
        for name in cuisine_names:
            cuisine, created = Cuisine.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created cuisine {name}'))
            cuisines.append(cuisine)
        
        # Create sample restaurants
        restaurant_data = [
            {
                'name': 'Bella Italia',
                'description': 'Authentic Italian cuisine with fresh pasta and wood-fired pizzas',
                'address': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'phone_number': '+12125551234',
                'email': 'info@bellaitalia.com',
                'rating': 4.5,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Dragon Palace',
                'description': 'Traditional Chinese dishes with modern twist',
                'address': '456 Oak Ave',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10002',
                'phone_number': '+12125555678',
                'email': 'info@dragonpalace.com',
                'rating': 4.2,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Taco Fiesta',
                'description': 'Authentic Mexican street food and margaritas',
                'address': '789 Pine St',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10003',
                'phone_number': '+12125559012',
                'email': 'info@tacofiesta.com',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Spice Garden',
                'description': 'Authentic Indian cuisine with a modern twist',
                'address': '101 Spice St',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10004',
                'phone_number': '+12125551111',
                'email': 'info@spicegarden.com',
                'rating': 4.6,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Taj Mahal Palace',
                'description': 'Royal Indian delicacies in a luxurious setting',
                'address': '202 Royal Ave',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10007',
                'phone_number': '+12125554444',
                'email': 'info@tajmahalpalace.com',
                'rating': 4.9,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Delhi Darbar',
                'description': 'Traditional North Indian street food and delicacies',
                'address': '303 Delhi St',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10008',
                'phone_number': '+12125555555',
                'email': 'info@delhidarbar.com',
                'rating': 4.7,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Sakura Sushi',
                'description': 'Fresh sushi and Japanese cuisine',
                'address': '202 Sakura Ave',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10005',
                'phone_number': '+12125552222',
                'email': 'info@sakurasushi.com',
                'rating': 4.8,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            },
            {
                'name': 'Le Bistro',
                'description': 'Classic French cuisine in an elegant setting',
                'address': '303 Bistro Blvd',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10006',
                'phone_number': '+12125553333',
                'email': 'info@lebistro.com',
                'rating': 4.4,
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
            }
        ]
        
        restaurants = []
        for i, data in enumerate(restaurant_data):
            if not Restaurant.objects.filter(name=data['name']).exists():
                # Extract image_url and remove it from data
                image_url = data.pop('image_url', None)
                
                # Use the first owner if owners list is not empty, otherwise use the first owner in the database
                owner = owners[i % len(owners)] if owners else User.objects.filter(is_restaurant_owner=True).first()
                if not owner:
                    # If no restaurant owners exist, use the first user
                    owner = User.objects.first()
                
                restaurant = Restaurant.objects.create(
                    owner=owner,
                    **data
                )
                restaurants.append(restaurant)
                self.stdout.write(self.style.SUCCESS(f'Created restaurant {restaurant.name}'))
                
                # Assign random cuisines to restaurant
                for cuisine in random.sample(cuisines, random.randint(1, 3)):
                    RestaurantCuisine.objects.get_or_create(
                        restaurant=restaurant,
                        cuisine=cuisine
                    )
                
                # Create sample menu items based on restaurant type
                if 'Italia' in restaurant.name:
                    menu_items = [
                        {'name': 'Margherita Pizza', 'price': 12.99, 'description': 'Classic pizza with tomato sauce and mozzarella'},
                        {'name': 'Spaghetti Carbonara', 'price': 15.99, 'description': 'Traditional Roman pasta dish'},
                        {'name': 'Lasagna', 'price': 14.99, 'description': 'Layered pasta with meat and cheese'},
                        {'name': 'Tiramisu', 'price': 7.99, 'description': 'Classic Italian dessert'},
                        {'name': 'Bruschetta', 'price': 8.99, 'description': 'Toasted bread topped with tomatoes and basil'},
                        {'name': 'Chicken Parmesan', 'price': 16.99, 'description': 'Breaded chicken with tomato sauce and cheese'},
                    ]
                elif 'Dragon' in restaurant.name:
                    menu_items = [
                        {'name': 'Sweet and Sour Chicken', 'price': 13.99, 'description': 'Crispy chicken with sweet and sour sauce'},
                        {'name': 'Beef and Broccoli', 'price': 14.99, 'description': 'Tender beef with fresh broccoli'},
                        {'name': 'Vegetable Spring Rolls', 'price': 6.99, 'description': 'Crispy rolls filled with fresh vegetables'},
                        {'name': 'Fried Rice', 'price': 9.99, 'description': 'Wok-fried rice with vegetables and egg'},
                        {'name': 'Kung Pao Chicken', 'price': 13.99, 'description': 'Spicy stir-fried chicken with peanuts'},
                        {'name': 'Hot and Sour Soup', 'price': 5.99, 'description': 'Traditional Chinese soup with tofu and mushrooms'},
                    ]
                elif 'Taco' in restaurant.name:
                    menu_items = [
                        {'name': 'Chicken Tacos', 'price': 10.99, 'description': 'Soft tacos with grilled chicken and salsa'},
                        {'name': 'Beef Quesadilla', 'price': 11.99, 'description': 'Grilled tortilla with beef and cheese'},
                        {'name': 'Guacamole', 'price': 7.99, 'description': 'Fresh avocado dip with chips'},
                        {'name': 'Churros', 'price': 6.99, 'description': 'Fried dough pastry with cinnamon sugar'},
                        {'name': 'Fish Tacos', 'price': 12.99, 'description': 'Battered fish with cabbage slaw and sauce'},
                        {'name': 'Margarita', 'price': 8.99, 'description': 'Classic cocktail with tequila and lime'},
                    ]
                elif 'Spice' in restaurant.name or 'Taj' in restaurant.name or 'Delhi' in restaurant.name:
                    menu_items = [
                        {'name': 'Chicken Tikka Masala', 'price': 15.99, 'description': 'Tender chicken in creamy tomato sauce'},
                        {'name': 'Vegetable Biryani', 'price': 12.99, 'description': 'Fragrant rice with mixed vegetables'},
                        {'name': 'Garlic Naan', 'price': 3.99, 'description': 'Soft bread baked in tandoor'},
                        {'name': 'Samosas', 'price': 5.99, 'description': 'Crispy pastries filled with spiced potatoes'},
                        {'name': 'Butter Chicken', 'price': 16.99, 'description': 'Creamy tomato-based curry with chicken'},
                        {'name': 'Gulab Jamun', 'price': 6.99, 'description': 'Sweet milk-based dessert balls'},
                        {'name': 'Paneer Tikka', 'price': 13.99, 'description': 'Grilled cottage cheese with spices'},
                        {'name': 'Dal Makhani', 'price': 11.99, 'description': 'Creamy black lentils with butter'},
                        {'name': 'Aloo Gobi', 'price': 10.99, 'description': 'Potatoes and cauliflower with spices'},
                        {'name': 'Chicken Biryani', 'price': 14.99, 'description': 'Fragrant rice with tender chicken'},
                        {'name': 'Palak Paneer', 'price': 12.99, 'description': 'Cottage cheese in spinach gravy'},
                        {'name': 'Tandoori Chicken', 'price': 15.99, 'description': 'Marinated chicken cooked in tandoor'},
                    ]
                elif 'Sakura' in restaurant.name:
                    menu_items = [
                        {'name': 'Salmon Sashimi', 'price': 18.99, 'description': 'Fresh salmon slices'},
                        {'name': 'California Roll', 'price': 9.99, 'description': 'Crab, avocado, and cucumber roll'},
                        {'name': 'Miso Soup', 'price': 4.99, 'description': 'Traditional soybean paste soup'},
                        {'name': 'Chicken Teriyaki', 'price': 14.99, 'description': 'Grilled chicken with sweet soy glaze'},
                        {'name': 'Edamame', 'price': 5.99, 'description': 'Steamed soybeans with sea salt'},
                        {'name': 'Green Tea Ice Cream', 'price': 6.99, 'description': 'Traditional Japanese dessert'},
                    ]
                elif 'Bistro' in restaurant.name:
                    menu_items = [
                        {'name': 'Coq au Vin', 'price': 19.99, 'description': 'Braised chicken with wine and mushrooms'},
                        {'name': 'Beef Bourguignon', 'price': 21.99, 'description': 'Slow-cooked beef stew'},
                        {'name': 'French Onion Soup', 'price': 7.99, 'description': 'Rich soup with melted cheese'},
                        {'name': 'Crème Brûlée', 'price': 8.99, 'description': 'Rich custard with caramelized sugar'},
                        {'name': 'Croissants', 'price': 4.99, 'description': 'Buttery flaky pastry'},
                        {'name': 'Ratatouille', 'price': 13.99, 'description': 'Vegetable stew from Provence'},
                    ]
                else:
                    menu_items = [
                        {'name': f'{restaurant.name} Special 1', 'price': random.uniform(10, 25), 'description': 'A delicious signature dish'},
                        {'name': f'{restaurant.name} Special 2', 'price': random.uniform(10, 25), 'description': 'Another delicious signature dish'},
                        {'name': 'Appetizer 1', 'price': random.uniform(5, 15), 'description': 'A tasty appetizer'},
                        {'name': 'Dessert 1', 'price': random.uniform(5, 10), 'description': 'A sweet dessert'},
                    ]
                
                for item_data in menu_items:
                    MenuItem.objects.create(
                        restaurant=restaurant,
                        **item_data
                    )
                
                # Create sample restaurant hours
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                for day_index, day in enumerate(days):
                    RestaurantHours.objects.create(
                        restaurant=restaurant,
                        day_of_week=day_index,
                        opening_time=time(10, 0),  # 10:00 AM
                        closing_time=time(22, 0),  # 10:00 PM
                        is_closed=(day_index == 6)  # Closed on Sunday
                    )
        
        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))