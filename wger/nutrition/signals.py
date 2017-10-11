from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from wger.nutrition.models import NutritionPlan, Meal, MealItem
from wger.utils.cache import cache_mapper


@receiver(post_save, sender=NutritionPlan)
@receiver(post_save, sender=Meal)
@receiver(post_save, sender=MealItem)
@receiver(post_delete, sender=NutritionPlan)
@receiver(post_delete, sender=Meal)
@receiver(post_delete, sender=MealItem)
def delete_cache(sender, **kwargs):
    model_instance = kwargs['instance']
    if sender == NutritionPlan:
        pk = model_instance.pk
    elif sender == Meal:
        pk = model_instance.plan.pk
    elif sender == MealItem:
        pk = model_instance.meal.plan.pk

    cache.delete(cache_mapper.get_nutrition_cache_key(pk))
    print('Cache deleted')
 
