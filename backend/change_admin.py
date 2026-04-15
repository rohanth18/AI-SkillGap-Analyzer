from app import app, db, User
from werkzeug.security import generate_password_hash

def change_admin_credentials(old_email, new_email, new_password, new_name=None):
    """Change admin credentials"""
    with app.app_context():
        # Find the admin user by email
        admin = User.query.filter_by(email=old_email).first()
        
        if not admin:
            print(f"[ERROR] User with email '{old_email}' not found!")
            return False
        
        if not admin.is_admin:
            print(f"[WARNING] User '{old_email}' is not an admin!")
            return False
        
        # Update credentials
        admin.email = new_email
        admin.password_hash = generate_password_hash(new_password)
        if new_name:
            admin.name = new_name
        
        db.session.commit()
        
        print("[SUCCESS] Admin credentials updated successfully!")
        print(f"   New Email: {new_email}")
        print(f"   New Name: {admin.name}")
        print(f"   Password: [Updated]")
        return True

def list_all_users():
    """List all users in the database"""
    with app.app_context():
        users = User.query.all()
        print("\nAll Users in Database:")
        print("-" * 60)
        for user in users:
            admin_badge = "[ADMIN]" if user.is_admin else "[USER]"
            print(f"{admin_badge} | ID: {user.id} | Email: {user.email} | Name: {user.name}")
        print("-" * 60)

if __name__ == "__main__":
    print("Admin Credentials Manager")
    print("=" * 60)
    
    # First, list all users
    list_all_users()
    
    print("\n" + "=" * 60)
    print("Enter new admin credentials:")
    print("=" * 60)
    
    old_email = input("Current admin email: ").strip()
    new_email = input("New admin email: ").strip()
    new_password = input("New admin password: ").strip()
    new_name = input("New admin name (press Enter to keep current): ").strip()
    
    if not new_name:
        new_name = None
    
    print("\n" + "=" * 60)
    success = change_admin_credentials(old_email, new_email, new_password, new_name)
    
    if success:
        print("\n[SUCCESS] You can now login with:")
        print(f"   Email: {new_email}")
        print(f"   Password: {new_password}")
