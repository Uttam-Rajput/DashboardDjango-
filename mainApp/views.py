from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mainApp.models import DataPoint  
from django.http import JsonResponse
from pymongo import MongoClient
from django.contrib import messages
from .models import User
import plotly.express as px
import json
import plotly.io as pio


def dashboard_view(request):
    return render(request, 'dashboard.html')


def fetch_data(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

        data = list(collection.find({}, {
            "_id": 0, "intensity": 1, "likelihood": 1, "relevance": 1,
            "year": 1, "country": 1, "topic": 1, "region": 1, "city": 1
        }))
        

        client.close()
        
        print("Fetched Data:", data)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def fetch_string_data(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

        # Get unique topics and regions
        unique_topics = collection.distinct("topic")
        unique_regions = collection.distinct("region")

        # Get their lengths
        unique_topics_count = len(unique_topics)
        unique_regions_count = len(unique_regions)

        client.close()

        return JsonResponse({
            "unique_topics_count": unique_topics_count,
            "unique_regions_count": unique_regions_count
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_chart_data(request):
    data = DataPoint.objects.all().values('name', 'value')
    return Response(list(data))


def chart(request):
    data = DataPoint.objects.all().values('name', 'value')

   
    import pandas as pd
    df = pd.DataFrame(list(data))

    fig = px.bar(df, x='name', y='value', title='Data Visualization')


    chart_json = fig.to_json()

    return render(request, 'chart.html', {'chart_json': chart_json})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username, password=password).first()

        if user:
            request.session["user_id"] = str(user.id) 
            messages.success(request, "Login successful!")
            return redirect("dashboard")  
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, "login.html")

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()  
    messages.success(request, "Logged out successfully!")
    return redirect("login")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "signup.html")

     
        user = User(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "signup.html")  

def average_intensity_chart(request):
    try:
       
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

        pipeline = [
            {"$group": {"_id": "$sector", "avg_intensity": {"$avg": "$intensity"}}},
            {"$sort": {"avg_intensity": -1}}
        ]
        data = list(collection.aggregate(pipeline))

        categories = [item["_id"] for item in data if item["_id"] is not None]
        avg_intensities = [item["avg_intensity"] for item in data]

        fig = px.bar(
            x=categories, y=avg_intensities, 
            labels={"x": "Sector", "y": "Avg Intensity"},
            title="Average Intensity by Sector",
            color=avg_intensities
        )

        graph_json = pio.to_json(fig)

        return JsonResponse({"graph": graph_json})

    except Exception as e:
        print("Error:", str(e))  
        return JsonResponse({"error": str(e)}, status=500)
    

def average_likelihood_chart(request):
    try:
        client = MongoClient("mongodb://localhost:27017/") 
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

        pipeline = [
            {"$group": {"_id": "$sector", "avg_likelihood": {"$avg": "$likelihood"}}},
            {"$sort": {"avg_likelihood": -1}}
        ]
        data = list(collection.aggregate(pipeline))

        print("Fetched Data:", data)

        categories = []
        avg_likelihoods = []

        for item in data:
            if item["_id"] is not None and isinstance(item["avg_likelihood"], (int, float)):
                categories.append(item["_id"])
                avg_likelihoods.append(item["avg_likelihood"])

        if not categories or not avg_likelihoods:
            return JsonResponse({"error": "No valid data found"}, status=500)

        fig = px.bar(
            x=categories, 
            y=avg_likelihoods, 
            labels={"x": "Sector", "y": "Avg Likelihood"},
            title="Average Likelihood by Sector",
            color=avg_likelihoods
        )
        graph_json = pio.to_json(fig)

        return JsonResponse({"graph": graph_json})

    except Exception as e:
        print("Error Occurred:", str(e))  
        return JsonResponse({"error": str(e)}, status=500)
    

def average_relevance_chart(request):
    try:
        
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

   
        pipeline = [
            {"$group": {"_id": "$sector", "avg_relevance": {"$avg": "$relevance"}}},
            {"$sort": {"avg_relevance": -1}}
        ]
        data = list(collection.aggregate(pipeline))

        categories = [item["_id"] for item in data if item["_id"] is not None]
        avg_relevances = [item["avg_relevance"] for item in data]

        fig = px.bar(
            x=categories, 
            y=avg_relevances, 
            labels={"x": "Sector", "y": "Avg Relevance"},
            title="Average Relevance by Sector",
            color=avg_relevances
        )

    
        graph_json = pio.to_json(fig)

        return JsonResponse({"graph": graph_json})

    except Exception as e:
        print("Error Occurred:", str(e))  
        return JsonResponse({"error": str(e)}, status=500)
    

def unique_topic_chart(request):
    try:
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

        pipeline = [
            {"$group": {"_id": "$topic", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        data = list(collection.aggregate(pipeline))

        topics = [item["_id"] for item in data if item["_id"] is not None]
        counts = [item["count"] for item in data]

        fig = px.bar(
            x=topics, y=counts,
            labels={"x": "Topics", "y": "Count"},
            title="Unique Topics Count",
            color=counts
        )

        graph_json = pio.to_json(fig)

        return JsonResponse({"graph": graph_json})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def unique_regions_chart(request):
    try:
      
        client = MongoClient("mongodb://localhost:27017/")
        db = client["maindb"]  
        collection = db["mainApp_dataentry"]  

  
        data = collection.distinct("region")

        region_counts = {region: collection.count_documents({"region": region}) for region in data}

        sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)

        regions = [item[0] for item in sorted_regions]
        counts = [item[1] for item in sorted_regions]

        fig = px.bar(
            x=regions, y=counts,
            labels={"x": "Region", "y": "Count"},
            title="Unique Regions Distribution",
            color=counts
        )

        graph_json = pio.to_json(fig)

        return JsonResponse({"graph": graph_json})

    except Exception as e:
        print("Error Occurred:", str(e))  
        return JsonResponse({"error": str(e)}, status=500)
