from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
app_name= "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("filter/", views.refined_view, name="refined_view"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("<int:user_id>/mylistings", views.mylistings, name="mylistings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("<int:user_id>/watchlist", views.watchlist_view, name="watchlist"),
    path("comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("bid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("add_to_watchlist/<int:listing_id>/<int:user_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>/<int:user_id>", views.remove_from_watchlist, name="remove_from_watchlist")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
