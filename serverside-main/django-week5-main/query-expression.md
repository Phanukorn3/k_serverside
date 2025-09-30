# Query Expressions

[Django Doc](https://docs.djangoproject.com/en/5.2/ref/models/expressions/#query-expressions)

ORM ของ Django นั้น support การใช้งาน function ในการคำนวณ (+, -, *, /) การ aggregate ต่างๆ เช่น SUM(), MIN(), MAX(), COUNT(), AVG() และการทำ Subquery

ซึ่งในส่วนนี้เราจะเรียกว่าการทำ Query Expression

สมมติเรามี model `Company` ดังนี้

```python
from datetime import date

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=20, null=True)
    num_employees = models.IntegerField()
    num_tables = models.IntegerField()
    num_chairs = models.IntegerField()

    def __str__(self):
        return self.name
```

เรามา setup project กันสำหรับ tutorial นี้

1. สร้าง project ใหม่ชื่อ `week5_tutorial` (สร้าง vitual environment ใหม่ด้วย)
2. สร้าง app ชื่อ `companies` และทำการตั้งค่าใน `settings.py`
3. แก้ไขไฟล์ `/companies/models.py` และเพิ่ม code ด้่านบนลงไป โดย models นี้เราจะใช้ในการทำ tutorial วันนี้กัน
4. `makemigrations` และ `migrate`

เปิด Django shell จากนั้นสร้างแถวข้อมูลด้วยคำสั่ง

```python
>>> from company.models
>>> Company.objects.create(name="Company AAA", num_employees=120, num_chairs=150, num_tables=60)
>>> Company.objects.create(name="Company BBB", num_employees=50, num_chairs=30, num_tables=20)
>>> Company.objects.create(name="Company CCC", num_employees=100, num_chairs=40, num_tables=40)
```

**ลองทดสอบคำสั่งด้านล่างนี้ดู แล้วดูสิว่าได้ผลลัพธ์เป็นอย่างไร**

```python
>>> from company.models import Company
>>> from django.db.models import Count, F, Value
>>> from django.db.models.functions import Length, Upper
>>> from django.db.models.lookups import GreaterThan

# Find companies that have more employees than chairs.
>>> Company.objects.filter(num_employees__gt=F("num_chairs"))

# Find companies that have at least twice as many employees as chairs.
>>> Company.objects.filter(num_employees__gt=F("num_chairs") * 2)

# Find companies that have more employees than the number of chairs and tables combined.
>>> Company.objects.filter(num_employees__gt=F("num_chairs") + F("num_tables"))

# How many chairs are needed for each company to seat all employees?
>>> company = (
...     Company.objects.filter(num_employees__gt=F("num_chairs"))
...     .annotate(chairs_needed=F("num_employees") - F("num_chairs"))
...     .first()
... )
>>> company.num_employees
50
>>> company.num_chairs
30
>>> company.chairs_needed
20
```

Django มี function ของ database ให้เรียกใช้ หลากหลาย เช่น

- Greatest: เปรียบเทียบค่า 2 ค่าโดยจะ return ค่าที่มากที่สุด (สามารถเปรียบเทียบได้มากกว่า 2 ค่า)

```python
class Blog(models.Model):
    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

---------------

>>> from django.db.models.functions import Greatest
>>> blog = Blog.objects.create(body="Greatest is the best.")
>>> comment = Comment.objects.create(body="No, Least is better.", blog=blog)
>>> comments = Comment.objects.annotate(last_updated=Greatest("modified", "blog__modified"))
```

- Now: เป็นเวลา server ณ เวลาปัจจุบัน

```python
>>> from django.db.models.functions import Now
>>> Article.objects.filter(published__lte=Now())
```

- Concat: ต่อค่าใน CharField หรือ TextField 2 ตัวหรือมากกว่าเข้าด้วยกัน

```python
>>> # Get the display name as "name (goes_by)"
>>> from django.db.models import CharField, Value as V
>>> from django.db.models.functions import Concat
>>> Author.objects.create(name="Margaret Smith", goes_by="Maggie")
>>> author = Author.objects.annotate(
...     screen_name=Concat("name", V(" ("), "goes_by", V(")"), output_field=CharField())
... ).get()
>>> print(author.screen_name)
Margaret Smith (Maggie)
```

ยังมีให้เลือกใช้อีกมากมาย สามารถดูใน document ได้เลยครับ

[Doc - Database Functions](https://docs.djangoproject.com/en/5.2/ref/models/database-functions/)

## Aggregate expression

สำหรับ tutorial นี้ให้ทำตามขั้นตอนนี้ 

1. สร้าง app ใหม่ชื่อ `books` ใน project `week5_tutorial` อันเดิม
2. เพิ่ม app books ใน `settings.py`
3. แก้ไขไฟล์ `/books/models.py` และเพิ่ม code ด้่านล่างลงไป โดย models เหล่านี้เราจะใช้ในการทำ tutorial นี้กัน
4. `makemigrations` และ `migrate`

```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Publisher(models.Model):
    name = models.CharField(max_length=300)


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
```

ทำการ import ข้อมูลเข้าตารางทั้งหมดด้วย SQL ในไฟล์ `books.sql`


**ลองทดสอบคำสั่งด้านล่างนี้ดู แล้วดูสิว่าได้ผลลัพธ์เป็นอย่างไร**

```python
>>> from books.models import Book
# Total number of books.
>>> Book.objects.count()
59

# Total number of books with publisher=Penguin Books
>>> Book.objects.filter(publisher__name="Penguin Books").count()
20

# Average price across all books, provide default to be returned instead
# of None if no books exist.
>>> from django.db.models import Avg
>>> Book.objects.aggregate(Avg("price", default=0))
{'price__avg': Decimal('9.7018644067796610')}

# Max price across all books, provide default to be returned instead of
# None if no books exist.
>>> from django.db.models import Max
>>> Book.objects.aggregate(Max("price", default=0))
{'price__max': Decimal('14.99')}

# All the following queries involve traversing the Book<->Publisher
# foreign key relationship backwards.

# Each publisher, each with a count of books as a "num_books" attribute.
>>> from books.models import Publisher
>>> from django.db.models import Count
>>> pubs = Publisher.objects.annotate(num_books=Count("book"))
>>> pubs
<QuerySet [<Publisher: BaloneyPress>, <Publisher: SalamiPress>, ...]>
>>> pubs[0].num_books
20

# Each publisher, with a separate count of books with a rating above and below 4
>>> from django.db.models import Q
>>> above = Publisher.objects.annotate(above_4=Count("book", filter=Q(book__rating__gt=4)))
>>> below = Publisher.objects.annotate(below_4=Count("book", filter=Q(book__rating__lte=4)))
>>> above[0].above_4
16
>>> below[0].below_4
4

# The top 5 publishers, in order by number of books.
>>> pubs = Publisher.objects.annotate(num_books=Count("book")).order_by("-num_books")[:5]
>>> pubs[0].num_books
39
```

### Generating aggregates over a QuerySet

ในกรณีที่เราต้องการคำนวณค่า summary ของ objects ทุกตัวใน QuerySet สามารถทำได้โดยการเรียก `aggregate()` และระบุว่าต้องการคำนวณค่า summary อะไร เช่น `Avg()`, `Max()`, `Min()`

```python
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.all().aggregate(Avg("price"))
{'price__avg': 34.35}

>>> Book.objects.aggregate(Avg("price"), Max("price"), Min("price"))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}
```

### Generating aggregates for *each item* in a QuerySet

สำหรับกรณีที่ต้องการคำนวณค่า summary ของแต่ละ record ใน QuerySet สามารถทำได้โดยการเรียก `annotate()` ยกตัวอย่างเช่นถ้าเราต้องการหาจำนวนผู้เขียน (`Author`) ของหนังสือ (`Book`) แต่ละเล่ม

```python
# Build an annotated queryset
>>> from django.db.models import Count
>>> q = Book.objects.annotate(num_authors=Count("authors"))
# Interrogate the first object in the queryset
>>> q[0]
<Book: The Definitive Guide to Django>
>>> q[0].num_authors
2
# Interrogate the second object in the queryset
>>> q[1]
<Book: Practical Django Projects>
>>> q[1].num_authors
1
```

เราสามารถ annotate หลายค่าได้ดังนี้

```python
>>> book = Book.objects.first()
>>> book.authors.count()
2
>>> book.store_set.count()
3
>>> q = Book.objects.annotate(Count("authors"), Count("store"))
>>> q[0].authors__count
6
>>> q[0].store__count
6
```

การ aggregate หลาย field จะได้ข้อมูลที่ไม่ถูกต้องเพราะเป็นการ join ทำให้ข้อมูลซ้ำซ้อน โดยสามารถแก้ไขได้โดยใช้ `distinct=True`

```python
>>> q = Book.objects.annotate(
...     Count("authors", distinct=True), Count("store", distinct=True)
... )
>>> q[0].authors__count
2
>>> q[0].store__count
3
```

เรายังสามารถใช้ `__` (double underscore notation) ได้ เพื่อ aggregate หรือ annotate ข้อมูลในตารางอื่นที่มีความสัมพันธ์กันอยู่ได้ เช่น

```python
>>> from django.db.models import Max, Min
>>> Store.objects.annotate(min_price=Min("books__price"), max_price=Max("books__price"))

>>> Store.objects.aggregate(youngest_age=Min("books__authors__age"))
```

### Using values()

การทำ aggregation group by สามารถทำได้โดยการใช้ `values()` เช่น

```python
>>> Author.objects.annotate(average_rating=Avg("book__rating"))

>>> Author.objects.values("name").annotate(average_rating=Avg("book__rating"))
```

ทั้งสอง statement ด้านบนนั้นแตกต่างกัน โดย statement แรกจะเป็นการ aggregate ค่า rating ของหนังสือของผู้เขียนทุกคนใน QuerySet แต่ใน stattment ที่สองจะเป็นการ ggregate ค่า rating ของหนังสือของผู้เขียนโดย group by `name` (ถ้ามีผู้เขียนที่ชื่อเหมือนกันจะนับเป็นคนเดียวกัน)

**การ group by ด้วย values() จะต้องเรียกใช้ values() ก่อน annotate()**

โดยถ้าวาง values() ไว้หลัง annotate จะเป็นการแปลง QuerySet เป็น list of dictionaries ซึ่งไม่เป็นการ group by

```python
>>> Author.objects.annotate(average_rating=Avg("book__rating")).values(
...     "name", "average_rating"
... )
```

## Subquery Expressions

นอกจากนั้น Django ORM ยังรองรับการทำ Subquery อีกด้วย

Subquery คืออะไร? เรามาดูตัวอย่างกัน 

Credit: [skooldio](https://blog.skooldio.com/how-to-use-subquery/)

สมมติเรามีตารางข้อมูลดังนี้

| name                       | studio    | year | gross |
|----------------------------|-----------|------|-------|
| ก้านกล้วย                  | กันตนา     | 2549 | 93.63 |
| ก้านกล้วย 2               | กันตนา     | 2552 | 79.26 |
| ฉลาดเกมส์โกง               | จีดีเอช ห้าห้าเก้า | 2560 | 112.15 |
| แฟนเดย์..แฟนกันแค่วันเดียว | จีดีเอช ห้าห้าเก้า | 2559 | 110.91 |
| พี่มาก..พระโขนง             | จีดีเอช     | 2556 | 559.59 |

เราสามารถเขียน Subquery ได้ดังตัวอย่าง

```sql
SELECT *,
      ( SELECT MAX(gross)
        FROM thai_boxoffice
        WHERE studio = m.studio
      ) AS studio_max_gross
FROM thai_boxoffice AS m 
ORDER BY studio, gross
```

ซึ่งจะได้ผลลัพธ์ดังนี้

| name                       | studio    | year | gross | studio_max_gross |
|----------------------------|-----------|------|-------|------------------|
| ก้านกล้วย                  | กันตนา     | 2549 | 93.63 | 93.63            |
| ก้านกล้วย 2               | กันตนา     | 2552 | 79.26 | 93.63            |
| ฉลาดเกมส์โกง               | จีดีเอช ห้าห้าเก้า | 2560 | 112.15 | 112.15           |
| แฟนเดย์..แฟนกันแค่วันเดียว | จีดีเอช ห้าห้าเก้า | 2559 | 110.91 | 112.15           |
| พี่มาก..พระโขนง             | จีดีเอช     | 2556 | 559.59 | 559.59           |


```sql
SELECT *
FROM thai_boxoffice AS m 
WHERE gross = ( SELECT MAX(gross)
                FROM thai_boxoffice
                WHERE studio = m.studio
              )
ORDER BY studio
```

ซึ่งจะได้ผลลัพธ์ดังนี้

| name                       | studio              | year | gross |
|----------------------------|---------------------|------|-------|
| ก้านกล้วย                  | กันตนา               | 2549 | 93.63 |
| ฉลาดเกมส์โกง               | จีดีเอช ห้าห้าเก้า   | 2560 | 112.15 |
| พี่มาก..พระโขนง             | จีดีเอช               | 2556 | 559.59 |


เข้าใจเรื่อง Subquery กันแล้วทีนี้เรามาดูกันว่า เราจำใช้งาน Subquery ใน Django ได้อย่างไร

สมมติเรามี models ดังนี้

```python
class Blog(models.Model):
    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    body = models.TextField()
    length = models.IntegerField(default=0)
    email = models.EmailField(null=True)
    modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
```

ถ้าเราต้องการหา email ของคนที่มา comment ใน blog ล่าสุด สามารถเขียนได้ดังนี้

```python
>>> from django.db.models import OuterRef, Subquery
>>> newest = Comment.objects.filter(blog=OuterRef("pk")).order_by("-created_at")
>>> Blog.objects.annotate(newest_commenter_email=Subquery(newest.values("email")[:1]))
```

จะแปลงเป็น SQL ได้ดังนี้

```sql
SELECT "blog"."id", (
    SELECT U0."email"
    FROM "comment" U0
    WHERE U0."blog_id" = ("blog"."id")
    ORDER BY U0."created_at" DESC LIMIT 1
) AS "newest_commenter_email" FROM "blog"
```

### Using aggregates within a Subquery expression

สมมติเราต้องการหาว่า blog แต่ละ blog นั้นมีขนาดความยาวของ comment รวมเป็นเท่าไหร่

```python
>>> from django.db.models import OuterRef, Subquery, Sum
>>> comments = Comment.objects.filter(blog=OuterRef("pk")).order_by().values("blog")
>>> total_comments = comments.annotate(total=Sum("length")).values("total")
>>> Post.objects.annotate(comment_length=Subquery(total_comments))
```
