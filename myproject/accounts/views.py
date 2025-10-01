import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from myproject.firebase_app import db  # Firestore db import
import datetime
import threading
from myproject.firebase_app import firebase_auth, db
from django.contrib import messages





FIREBASE_WEB_API_KEY = "AIzaSyDJPMXFp3rjjX9tD35UEGUKtAEk-UpvcSU"

def fetch_users_with_timeout(timeout=3):
    users_list = []

    def fetch():
        nonlocal users_list
        try:
            users = db.collection("users").limit(10).get()
            users_list = [{**u.to_dict(), "id": u.id} for u in users]
        except Exception as e:
            print("❌ Firestore fetch error:", e)

    thread = threading.Thread(target=fetch)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("⏱️ Firestore fetch timed out after", timeout, "seconds")
        thread.join(0)  # stop waiting
        return None  # timeout case
    return users_list

# =====================
# Home Page
# =====================

def home(request):
    users_list = []
    try:
        users = db.collection("users").get()
        for user in users:
            user_data = user.to_dict()
            users_list.append({
                "id": user.id,
                "name": user_data.get("name", "Not Provided"),
                "email": user_data.get("email", "Not Provided"),
                "phone": user_data.get("phone", "Not Provided"),
                "gender": user_data.get("gender", "Not Provided"),
                "address": user_data.get("address", "Not Provided"),
            })
    except Exception as e:
        print("🔥 Firestore fetch error:", e)
        messages.error(request, f"Error fetching users: {e}")

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

        try:
            user = firebase_auth.create_user(
                email=email,
                password=password,
                display_name=name
            )

            db.collection("users").document(user.uid).set({
                "name": name,
                "email": email,
                "phone": phone,
                "gender": gender,
                "address": address,
                "created_at": datetime.datetime.now().isoformat()
            })

            messages.success(request, "Signup successful ✅")
            return redirect("login")

        except Exception as e:
            messages.error(request, f"Signup failed: {e}")
            return redirect("signup")

    return render(request, "accounts/signup.html")
# def signup(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         phone = request.POST.get("phone")
#         gender = request.POST.get("gender")
#         address = request.POST.get("address")
#
#         if not (name and email and password):
#             messages.error(request, "Name, Email and Password are required!")
#             return redirect("signup")
#
#         try:
#             user_ref = db.collection('users').document()
#             user_ref.set({
#                 'name': name,
#                 'email': email,
#                 'password': password,  # ⚠️ Demo, encrypt in real project
#                 'phone': phone,
#                 'gender': gender,
#                 'address': address,
#                 'created_at': datetime.datetime.now().isoformat()
#             })
#
#             messages.success(request, "Signup successful ✅")
#             return redirect("home")
#
#         except Exception as e:
#             messages.error(request, f"Signup failed: {e}")
#             return redirect("signup")
#
#     return render(request, "accounts/signup.html")


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


# def login_view(request):
#     return render(request, "accounts/login.html")
import requests



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            res = requests.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}",
                json={
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                },
            )
            res_data = res.json()

            if "idToken" in res_data:
                request.session['uid'] = res_data['localId']
                messages.success(request, "✅ Login successful")
                return redirect("home")
            else:
                error_msg = res_data.get("error", {}).get("message", "Login failed")
                messages.error(request, f"❌ {error_msg}")

        except Exception as e:
            messages.error(request, f"❌ Error: {e}")

    return render(request, "accounts/login.html")

