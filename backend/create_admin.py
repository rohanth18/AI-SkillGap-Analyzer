from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin(name, email, password):
    with app.app_context():
        # Check if user already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"❌ User with email '{email}' already exists!")
            return False
        
        # Create new admin
        admin = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ New admin created successfully!")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        return True

if __name__ == "__main__":
    print("👑 Create New Admin User")
    print("=" * 60)
    
    name = input("Admin name: ").strip()
    email = input("Admin email: ").strip()
    password = input("Admin password: ").strip()
    
    print("\n" + "=" * 60)
    create_admin(name, email, password)
