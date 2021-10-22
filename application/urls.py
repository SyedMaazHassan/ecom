from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'application'

urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.home, name="home"),
    path('category/<int:id>', views.category, name="category"),
    path('products/<int:id>', views.detail, name="products"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('sign-in/', views.sign_in, name="sign_in"),
    path('all_categories', views.all_categories, name='all_categories'),
    path('all-categories/', views.all_categories, name='all-categories'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('profile/', views.profile, name='profile'),
    path('all-products/', views.all_products, name='all-products'),
    path('mark-as-favorite', views.mark_as_favorite, name="mark-as-favorite"),
    path('get-favorites', views.get_favorites, name="get-favorites"),
    # path('signup', views.signup, name="signup"),
    # path('login', views.login, name="login"),
    # path('logout', views.logout, name="logout"),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
