from app import app, db, User

with app.app_context():
    admins = User.query.filter_by(is_admin=True).all()
    
    print("\n👑 Current Admin Users:")
    print("=" * 60)
    
    if not admins:
        print("No admin users found!")
    else:
        for admin in admins:
            print(f"ID: {admin.id}")
            print(f"Name: {admin.name}")
            print(f"Email: {admin.email}")
            print(f"Created: {admin.created_at}")
            print("-" * 60)
    
    print(f"\nTotal Admin Users: {len(admins)}")
