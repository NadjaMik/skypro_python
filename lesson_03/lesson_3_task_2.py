from smartphone import Smartphone
smartphone1 = Smartphone("Nokia", "3310", "+7-921-111-11-11")
smartphone2 = Smartphone("Siemens", "A51", "+7-911-222-22-22")
smartphone3 = Smartphone("LG", "TG34", "+7-981-333-33-33")
smartphone4 = Smartphone("Samsung", "s26", "+7-921-444-44-44")
smartphone5 = Smartphone("Alcatel", "a45", "+7-904-555-55-55")
catalog = [smartphone1, smartphone2, smartphone3, smartphone4, smartphone5]

le = len(catalog)

for n in range(le):
    print(catalog[n])
