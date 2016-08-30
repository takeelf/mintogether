# Minimum together Validation in django rest framework

django rest framework validation

### example
```sh
class SomeSerializer(serializers.ModelSerializer):
    class Meta:
        validators = [
            MinTogetherValidator(
                fields=('field1', 'field2'),
                min=1000 # minimum amount
            )
        ]
```
