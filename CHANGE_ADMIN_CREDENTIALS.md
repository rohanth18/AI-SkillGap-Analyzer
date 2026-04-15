# 🔐 How to Change Admin Credentials

## 📋 **Available Methods**

There are 3 ways to change admin credentials:
1. **Method 1:** Using Python Script (Recommended - Easiest)
2. **Method 2:** Direct Database Editing (Advanced)
3. **Method 3:** Through Application (If logged in)

---

## ✅ **Method 1: Using Python Script (RECOMMENDED)**

This is the easiest and safest method.

### **Step 1: Create a script file**

Create a file named `change_admin.py` in the `project_v2/backend/` folder with this content:

```python
from app import app, db, User
from werkzeug.security import generate_password_hash

def change_admin_credentials(old_email, new_email, new_password, new_name=None):
    """Change admin credentials"""
    with app.app_context():
        # Find the admin user by email
        admin = User.query.filter_by(email=old_email).first()
        
        if not admin:
            print(f"❌ Error: User with email '{old_email}' not found!")
            return False
        
        if not admin.is_admin:
            print(f"⚠️  Warning: User '{old_email}' is not an admin!")
            return False
        
        # Update credentials
        admin.email = new_email
        admin.password_hash = generate_password_hash(new_password)
        if new_name:
            admin.name = new_name
        
        db.session.commit()
        
        print("✅ Admin credentials updated successfully!")
        print(f"   New Email: {new_email}")
        print(f"   New Name: {admin.name}")
        print(f"   Password: [Updated]")
        return True

def list_all_users():
    """List all users in the database"""
    with app.app_context():
        users = User.query.all()
        print("\n📋 All Users in Database:")
        print("-" * 60)
        for user in users:
            admin_badge = "👑 ADMIN" if user.is_admin else "👤 USER"
            print(f"{admin_badge} | ID: {user.id} | Email: {user.email} | Name: {user.name}")
        print("-" * 60)

if __name__ == "__main__":
    print("🔐 Admin Credentials Manager")
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
        print("\n✅ You can now login with:")
        print(f"   Email: {new_email}")
        print(f"   Password: {new_password}")
```

### **Step 2: Run the script**

**Windows:**
```powershell
cd "d:\Mca Main project just user module\Mca Main project just user module\project_v2\backend"
venv_new\Scripts\python.exe change_admin.py
```

**Mac/Linux:**
```bash
cd project_v2/backend
source venv_new/bin/activate
python change_admin.py
```

### **Step 3: Follow the prompts**

The script will:
1. Show all users in the database
2. Ask for current admin email
3. Ask for new email, password, and name
4. Update the credentials

---

## 🔧 **Method 2: Direct Database Editing (Advanced)**

### **Using SQLite Browser:**

1. **Download DB Browser for SQLite:**
   - https://sqlitebrowser.org/

2. **Open the database:**
   - Navigate to: `project_v2/backend/instance/skillgap.db`
   - Open with DB Browser

3. **Browse Data:**
   - Click "Browse Data" tab
   - Select "users" table

4. **Find Admin User:**
   - Look for user with `is_admin = 1`

5. **Update Email:**
   - Double-click the email cell
   - Enter new email
   - Click "Write Changes"

6. **Update Password:**
   - You need to generate a password hash first
   - See "Generate Password Hash" section below

### **Generate Password Hash:**

Create a file `generate_hash.py` in backend folder:

```python
from werkzeug.security import generate_password_hash

password = input("Enter new password: ")
hash_value = generate_password_hash(password)
print(f"\nPassword Hash:\n{hash_value}")
print("\nCopy this hash and paste it in the password_hash column")
```

Run it:
```powershell
venv_new\Scripts\python.exe generate_hash.py
```

---

## 🌐 **Method 3: Through Application (If Logged In)**

Currently, the application doesn't have a built-in "Change Password" feature in the UI. You would need to add this functionality.

### **Quick API Method (Using Browser Console):**

If you're logged in as admin:

1. Open browser console (F12)
2. Get your current token from localStorage
3. Use this code:

```javascript
// This would require adding a change password endpoint to the backend first
// Not currently available in the application
```

**Note:** This method requires backend API endpoint development.

---

## 🚀 **Quick Commands (Copy-Paste)**

### **Windows - Change Admin Credentials:**

```powershell
# Navigate to backend
cd "d:\Mca Main project just user module\Mca Main project just user module\project_v2\backend"

# Create the change_admin.py script (copy content from Method 1 above)
# Then run:
venv_new\Scripts\python.exe change_admin.py
```

### **Mac/Linux - Change Admin Credentials:**

```bash
# Navigate to backend
cd project_v2/backend

# Create the change_admin.py script (copy content from Method 1 above)
# Then run:
source venv_new/bin/activate
python change_admin.py
```

---

## 📝 **Alternative: Create New Admin**

If you want to create a NEW admin account instead:

Create `create_admin.py`:

```python
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
    
    create_admin(name, email, password)
```

Run it:
```powershell
venv_new\Scripts\python.exe create_admin.py
```

---

## 🔍 **View Current Admin:**

Create `view_admin.py`:

```python
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
```

Run it:
```powershell
venv_new\Scripts\python.exe view_admin.py
```

---

## ⚠️ **Important Notes:**

1. **Stop the backend server** before running database scripts (press Ctrl+C in backend terminal)
2. **Restart the backend** after making changes
3. **Passwords are hashed** - you cannot see the actual password in the database
4. **Email must be unique** - cannot have duplicate emails
5. **Backup your database** before making changes (copy `instance/skillgap.db`)

---

## 🛡️ **Security Best Practices:**

- ✅ Use strong passwords (min 8 characters, mix of letters, numbers, symbols)
- ✅ Don't share admin credentials
- ✅ Change default passwords immediately
- ✅ Keep backup of database before changes
- ✅ Delete script files after use (they may contain passwords)

---

## 📞 **Need Help?**

If you encounter any issues:
1. Make sure the backend server is stopped
2. Check that you're in the correct directory
3. Verify the virtual environment is activated
4. Check database file exists at `backend/instance/skillgap.db`

---

**Last Updated:** December 14, 2025
