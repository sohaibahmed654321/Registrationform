from django.shortcuts import render, redirect
from django.contrib import messages
from myproject.firebase_app import db
import datetime


# =====================
# Home Page (Splash + Data)
# =====================
def home(request):
    # Firestore se users fetch
    users = db.collection("users").stream()
    users_list = [{**u.to_dict(), "id": u.id} for u in users]

    # accounts/home.html render karo
    return render(request, "accounts/home.html", {"users": users_list})


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

        try:
            # Firestore me save karo
            user_ref = db.collection('users').document()
            user_ref.set({
                'name': name,
                'email': email,
                'password': password,  # ❗ demo purpose, real project me encrypt karna hoga
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
