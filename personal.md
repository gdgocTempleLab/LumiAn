# Todo 

1. update backend/.env
```
DATABASE_URL=postgresql://postgres:密碼@db.xxxxx.supabase.co:5432/postgres?sslmode=require
```
2. 做資料庫的反向migration
``` bash
python manage.py inspectdb > system\supabase_models.py
```
3. 資料表要注意managed = False
```
class Meta:
    managed = False
    db_table = "表名"
```