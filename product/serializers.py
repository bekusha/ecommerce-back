from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    recommended_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'description', 'price', 'quantity',  'created_at', 'image1', 'image2', 'image3', 'image4', 'image5', 'viscosity', 'liter','category', 'recommended_quantity']
        read_only_fields = ['vendor']

    def get_recommended_quantity(self, obj):
        required_liters = self.context.get('required_liters', 4)  # OpenAI-ს მიერ დაბრუნებული საჭირო ლიტრაჟი

        if not obj.liter or obj.liter <= 0:  # თუ `liter` არის `None` ან 0, ვაბრუნებთ 1-ს
            return 1  

        # ვიღებთ ყველა ხელმისაწვდომ ბოთლის ზომას
        all_products = self.context.get('all_products', [])
        bottle_sizes = sorted(set([p.liter for p in all_products if p.liter]), reverse=True)

        if not bottle_sizes:  # თუ ბოთლების ზომები არ არსებობს, ავტომატურად 1 ბოთლი დავაბრუნოთ
            return 1  

        remaining_liters = required_liters
        selected_bottles = {}

        # ჯერ ვირჩევთ ყველაზე დიდ ბოთლებს, რათა მინიმალური ბოთლის რაოდენობა გამოვიყენოთ
        for size in bottle_sizes:
            if remaining_liters <= 0:
                break
            count = remaining_liters // size
            if count > 0:
                selected_bottles[size] = int(count)
                remaining_liters -= count * size

        # **თუ მაინც დარჩა ლიტრაჟი, ვამატებთ ყველაზე პატარა ბოთლიდან**
        if remaining_liters > 0:
            smallest_size = min(bottle_sizes)  # **აქ უკვე შეცდომა აღარ იქნება!**
            selected_bottles[smallest_size] = selected_bottles.get(smallest_size, 0) + 1

        return selected_bottles.get(obj.liter, 0)  # ვაბრუნებთ მხოლოდ ამ კონკრეტული პროდუქტის რაოდენობას

    def create(self, validated_data):
            # `recommended_quantity` ითვლება `get_recommended_quantity`-ის საშუალებით
            instance = super().create(validated_data)
            instance.quantity = self.get_recommended_quantity(instance)  # `quantity` ველის განახლება
            instance.save()
            return instance

    def update(self, instance, validated_data):
            instance = super().update(instance, validated_data)
            instance.quantity = self.get_recommended_quantity(instance)  # `quantity` ველის განახლება
            instance.save()
            return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']