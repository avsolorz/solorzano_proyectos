from rest_framework import serializers
from proyectos.models import RedSocial


class RedSocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = RedSocial
        fields = ["id", "nombre_red"]
        read_only_fields = ["id"]


class RedSocialResumenSerializer(serializers.ModelSerializer):

    class Meta:
        model = RedSocial
        fields = ["id", "nombre_red"]
        read_only_fields = ["id"]
