from django.http import JsonResponse
from django.conf import settings


def get_products(request):
    try:
        collection = settings.MONGO_DB["Products"]

        # ---- Filters ----
        filters = {}

        # Accept comma-separated values for multi-filter support
        name = request.GET.get("name")
        categories = request.GET.get("category")  # could be comma separated
        brands = request.GET.get("brand")         # could be comma separated
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        # Name filter with regex (single value)
        if name:
            filters["product_name"] = {"$regex": name, "$options": "i"}

        # Multi-category filter
        if categories:
            category_list = categories.split(",")
            filters["categories"] = {"$in": category_list}

        # Multi-brand filter
        if brands:
            brand_list = brands.split(",")
            filters["company"] = {"$in": brand_list}

        # Price filters
        if min_price:
            filters["price"] = {"$gte": float(min_price)}
        if max_price:
            filters.setdefault("price", {})["$lte"] = float(max_price)

        # ---- Pagination ----
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))
        skip = (page - 1) * limit

        total_count = collection.count_documents(filters)

        products = list(
            collection.find(filters, {"_id": 0})
            .skip(skip)
            .limit(limit)
        )

        return JsonResponse({
            "success": True,
            "page": page,
            "limit": limit,
            "total": total_count,
            "total_pages": (total_count + limit - 1) // limit,
            "data": products
        }, safe=False)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
