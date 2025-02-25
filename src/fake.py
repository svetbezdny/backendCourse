from faker import Faker

fake = Faker(["ru_RU", "en_US"])

fake_hotels = []
for i in range(10):
    f = {"title": fake.company(), "location": fake.city()}
    fake_hotels.append(f)
