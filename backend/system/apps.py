import os
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_superuser(sender, **kwargs):
    """
    建立預設管理員帳號的邏輯
    會在資料庫遷移 (migrate) 完成後自動執行
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    # 可以透過環境變數自訂，若無則使用預設值
    username = os.environ.get("DEFAULT_ADMIN", "admin")
    password = os.environ.get("DEFAULT_PASSWORD", "admin")

    # 檢查該帳號是否已經存在，如果不存在就建立
    if not User.objects.filter(username=username).exists():
        print(f"[*] 系統初始化：正在建立預設管理員帳號 ({username})...")
        User.objects.create_superuser(username=username, password=password)


class SystemConfig(AppConfig):
    name = "system"

    def ready(self):
        # 將建立預設帳號的函式綁定到 post_migrate 訊號上
        post_migrate.connect(create_default_superuser, sender=self)
