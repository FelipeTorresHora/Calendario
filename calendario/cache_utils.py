from django.core.cache import cache
from django.conf import settings

class CacheManager:
    """Utility class for managing cache operations"""
    
    # Cache key patterns
    DASHBOARD_DATA = 'dashboard_data_{user_id}'
    DASHBOARD_METRICS = 'dashboard_metrics_{user_id}'
    USER_TASKS = 'user_tasks_{user_id}'
    TASK_DAY = 'tasks_day_{user_id}_{date}'
    
    @classmethod
    def get_user_cache_keys(cls, user_id):
        """Get all cache keys for a specific user"""
        return [
            cls.DASHBOARD_DATA.format(user_id=user_id),
            cls.DASHBOARD_METRICS.format(user_id=user_id),
            cls.USER_TASKS.format(user_id=user_id),
        ]
    
    @classmethod
    def invalidate_user_cache(cls, user_id):
        """Invalidate all cache entries for a specific user"""
        keys = cls.get_user_cache_keys(user_id)
        cache.delete_many(keys)
    
    @classmethod
    def get_or_set(cls, key, callable_func, timeout=300):
        """Get from cache or set if not exists"""
        data = cache.get(key)
        if data is None:
            data = callable_func()
            cache.set(key, data, timeout)
        return data
    
    @classmethod
    def clear_all_cache(cls):
        """Clear all cache (use with caution)"""
        cache.clear()

def cache_key_for_user(pattern, user_id, **kwargs):
    """Helper function to generate cache keys for users"""
    return pattern.format(user_id=user_id, **kwargs)