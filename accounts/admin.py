# ========================
# 9. ADMIN CONFIGURATION
# ========================

# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPreferences

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'native_language', 'target_language', 
                   'current_level', 'total_xp', 'is_premium', 'date_joined']
    list_filter = ['native_language', 'target_language', 'current_level', 'is_premium']
    search_fields = ['username', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Language Learning', {
            'fields': ('native_language', 'target_language', 'current_level', 
                      'total_xp', 'current_streak', 'best_streak')
        }),
        ('Premium', {
            'fields': ('is_premium', 'premium_expires_at')
        }),
    )

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'notifications_enabled', 'reminder_time', 'dark_mode']
    list_filter = ['notifications_enabled', 'dark_mode']
