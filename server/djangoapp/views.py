from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from django.contrib.auth.decorators import login_required
import json
import logging

logger = logging.getLogger(__name__)


# -------- Dealerships --------
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + str(dealer_id)
    dealer = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealer})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail["review"])
            review_detail["sentiment"] = sentiment.get("sentiment", "neutral")
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# -------- Post a Review --------
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})