room = EnterInSystem.Apartments()
            room.undergrounds = undergrounds
            room.address = adress
            room.discription = opisanie
            room.photo = fotoochka
            colcomn = colcomn.split()
            del colcomn[len(colcomn-1)]
            room.room = colcomn
            room.link = site
            price[:price.find('₽/мес.')]
            room.price = price
            room.area = obshplo.split()[0]
            room.items = items
            room.ucan = ucan