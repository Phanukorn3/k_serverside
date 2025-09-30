# serverside
import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

# import modules
from shop.models import *
from django.db.models import F, Q, Value as V, Count, OuterRef, Subquery, Avg, Sum, Min, Max
from django.db.models.functions import Concat, JSONObject
import json
from datetime import datetime
