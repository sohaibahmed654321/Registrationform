from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from myproject.firebase_app import db  # Firestore db import
import datetime

# =====================
# Home Page
# =====================
def home(request):
    try:
        users = db.collection("users").stream()
        users_list = [{**u.to_dict(), "id": u.id} for u in users]
    except Exception as e:
        messages.error(request, f"Failed to fetch users: {e}")
        users_list = []

    return render(request, "accounts/home.html", {"users": users_list})


def test_firebase(request):
    doc_ref = db.collection("test_users").document("demo_user")
    doc_ref.set({
        "name": "Sohaib",
        "email": "sohaib@example.com"
    })
    return HttpResponse("✅ Firebase connected with keys1.json!")


# =====================
# Signup Page
# =====================
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        address = request.POST.get("address")

        if not (name and email and password):
            messages.error(request, "Name, Email and Password are required!")
            return redirect("signup")

        try:
            user_ref = db.collection('users').document()
            user_ref.set({
                'name': name,
                'email': email,
                'password': password,  # ⚠️ Demo, encrypt in real project
                'phone': phone,
                'gender': gender,
                'address': address,
                'created_at': datetime.datetime.now().isoformat()
            })

            messages.success(request, "Signup successful ✅")
            return redirect("home")

        except Exception as e:
            messages.error(request, f"Signup failed: {e}")
            return redirect("signup")

    return render(request, "accounts/signup.html")


# =====================
# Signup Success Page
# =====================
def signup_success(request):
    return render(request, "accounts/signup_success.html")


# =====================
# Edit User
# =====================
def edit_user(request, user_id):
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        messages.error(request, "User not found ❌")
        return redirect("home")

    if request.method == "POST":
        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "gender": request.POST.get("gender"),
            "address": request.POST.get("address"),
        }
        user_ref.update(data)
        messages.success(request, "User updated successfully ✅")
        return redirect("home")

    return render(request, "accounts/edit_user.html", {
        "id": user_id,
        "user": user_doc.to_dict()
    })


# =====================
# Delete User
# =====================
def delete_user(request, user_id):
    user_ref = db.collection("users").document(user_id)
    user_ref.delete()
    messages.success(request, "User deleted successfully ❌")
    return redirect("home")


def login_view(request):
    return render(request, "accounts/login.html")
