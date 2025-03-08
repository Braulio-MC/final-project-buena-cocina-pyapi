import json
from core.firebaseHelper import db

productos = [
{
    "id": "prod001",
    "name": "Pizza Margarita",
    "description": "Deliciosa pizza con salsa de tomate, mozzarella y albahaca fresca.",
    "image": "https://example.com/images/pizza_margarita.jpg",
    "price": 150,
    "available": True,
    "store": {
      "id": "store001",
      "name": "Pizzería Bella Napoli"
    },
    "category": ["Italiana", "Pizza"],
    "discount": {
      "id": "disc001",
      "percentage": 10,
      "startDate": "2025-02-20T00:00:00Z",
      "endDate": "2025-02-28T23:59:59Z"
    },
    "rating": 4.5,
    "totalRating": 150,
    "totalReviews": 45,
    "paginationKey": "page1",
    "createdAt": "2025-02-15T12:00:00Z",
    "updatedAt": "2025-02-20T10:00:00Z"
  },
  {
    "id": "prod002",
    "name": "Hamburguesa Clásica",
    "description": "Jugosa hamburguesa con carne de res, lechuga, tomate y queso cheddar.",
    "image": "https://example.com/images/hamburguesa_clasica.jpg",
    "price": 120,
    "available": True,
    "store": {
      "id": "store002",
      "name": "Burger House"
    },
    "category": ["Americana", "Hamburguesas"],
    "discount": {
      "id": "disc002",
      "percentage": 15,
      "startDate": "2025-02-22T00:00:00Z",
      "endDate": "2025-03-05T23:59:59Z"
    },
    "rating": 4.7,
    "totalRating": 200,
    "totalReviews": 60,
    "paginationKey": "page1",
    "createdAt": "2025-02-10T14:00:00Z",
    "updatedAt": "2025-02-20T11:00:00Z"
  },
  {
    "id": "prod003",
    "name": "Tacos al Pastor",
    "description": "Tradicionales tacos mexicanos con carne al pastor, piña y cebolla.",
    "image": "https://example.com/images/tacos_al_pastor.jpg",
    "price": 90,
    "available": True,
    "store": {
      "id": "store003",
      "name": "Taquería El Buen Pastor"
    },
    "category": ["Mexicana", "Tacos"],
    "discount": {
      "id": "disc003",
      "percentage": 0,
      "startDate": None,
      "endDate": None
    },
    "rating": 4.8,
    "totalRating": 300,
    "totalReviews": 90,
    "paginationKey": "page1",
    "createdAt": "2025-02-12T16:00:00Z",
    "updatedAt": "2025-02-20T09:00:00Z"
  },
  {
    "id": "prod004",
    "name": "Sushi Variado",
    "description": "Bandeja de sushi variado con nigiri, maki y sashimi.",
    "image": "https://example.com/images/sushi_variado.jpg",
    "price": 250,
    "available": True,
    "store": {
      "id": "store004",
      "name": "Sushi Master"
    },
    "category": ["Japonesa", "Sushi"],
    "discount": {
      "id": "disc004",
      "percentage": 20,
      "startDate": "2025-02-25T00:00:00Z",
      "endDate": "2025-03-10T23:59:59Z"
    },
    "rating": 4.6,
    "totalRating": 180,
    "totalReviews": 55,
    "paginationKey": "page1",
    "createdAt": "2025-02-08T13:00:00Z",
    "updatedAt": "2025-02-20T12:00:00Z"
  },
  {
    "id": "prod005",
    "name": "Ensalada César",
    "description": "Ensalada fresca con lechuga romana, pollo a la parrilla, crotones y aderezo César.",
    "image": "https://example.com/images/ensalada_cesar.jpg",
    "price": 80,
    "available": True,
    "store": {
      "id": "store005",
      "name": "Healthy Bites"
    },
    "category": ["Saludable", "Ensaladas"],
    "discount": {
      "id": "disc005",
      "percentage": 5,
      "startDate": "2025-02-18T00:00:00Z",
      "endDate": "2025-02-28T23:59:59Z"
    },
    "rating": 4.2,
    "totalRating": 120,
    "totalReviews": 30,
    "paginationKey": "page1",
    "createdAt": "2025-02-05T15:00:00Z",
    "updatedAt": "2025-02-20T08:00:00Z"
  },
  {
    "id": "prod006",
    "name": "Spaghetti a la Boloñesa",
    "description": "Pasta italiana con salsa boloñesa casera y queso parmesano.",
    "image": "https://example.com/images/spaghetti_bolonesa.jpg",
    "price": 130,
    "available": True,
    "store": {
      "id": "store001",
      "name": "Pizzería Bella Napoli"
    },
    "category": ["Italiana", "Pasta"],
    "discount": {
      "id": "disc006",
      "percentage": 10,
      "startDate": "2025-02-20T00:00:00Z",
      "endDate": "2025-03-01T23:59:59Z"
    },
    "rating": 4.4,
    "totalRating": 160,
    "totalReviews": 40,
    "paginationKey": "page1",
    "createdAt": "2025-02-11T12:00:00Z",
    "updatedAt": "2025-02-20T10:30:00Z"
  },
  {
    "id": "prod007",
    "name": "Ramen Tradicional",
    "description": "Sopa japonesa con fideos, cerdo chashu, huevo y alga nori.",
    "image": "https://example.com/images/ramen_tradicional.jpg",
    "price": 180,
    "available": False,
    "store": {
      "id": "store004",
      "name": "Sushi Master"
    },
    "category": ["Japonesa", "Sopas"],
    "discount": {
      "id": "disc007",
      "percentage": 0,
      "startDate": None,
      "endDate": None
    },
    "rating": 4.9,
    "totalRating": 250,
    "totalReviews": 75,
    "paginationKey": "page1",
    "createdAt": "2025-02-07T17:00:00Z",
    "updatedAt": "2025-02-19T14:00:00Z"
  },
  {
    "id": "prod008",
    "name": "Chilaquiles Verdes",
    "description": "Totopos bañados en salsa verde, acompañados de pollo, crema y queso.",
    "image": "https://example.com/images/chilaquiles_verdes.jpg",
    "price": 95,
    "available": True,
    "store": {
      "id": "store006",
      "name": "Desayunos La Abuela"
    },
    "category": ["Mexicana", "Desayuno"],
    "discount": {
      "id": "disc008",
      "percentage": 5,
      "startDate": "2025-02-21T00:00:00Z",
      "endDate": "2025-03-03T23:59:59Z"
    },
    "rating": 4.3,
    "totalRating": 110,
    "totalReviews": 28,
    "paginationKey": "page1",
    "createdAt": "2025-02-06T09:00:00Z",
    "updatedAt": "2025-02-20T09:30:00Z",
  },
{
    "id": "prod009",
    "name": "Pad Thai",
    "description": "Fideos de arroz salteados con pollo, huevo, brotes de soja y maní.",
    "image": "https://example.com/images/pad_thai.jpg",
    "price": 140,
    "available": True,
    "store": {
      "id": "store007",
      "name": "Thai Express"
    },
    "category": ["Tailandesa", "Fideos"],
    "discount": {
      "id": "disc009",
      "percentage": 12,
      "startDate": "2025-02-23T00:00:00Z",
      "endDate": "2025-03-06T23:59:59Z"
    },
    "rating": 4.5,
    "totalRating": 130,
    "totalReviews": 40,
    "paginationKey": "page1",
    "createdAt": "2025-02-10T13:00:00Z",
    "updatedAt": "2025-02-20T11:30:00Z"
  },
  {
    "id": "prod010",
    "name": "Arepa Reina Pepiada",
    "description": "Arepa venezolana rellena de pollo, aguacate y mayonesa.",
    "image": "https://example.com/images/arepa_reina_pepiada.jpg",
    "price": 85,
    "available": True,
    "store": {
      "id": "store008",
      "name": "Sabores Latinos"
    },
    "category": ["Venezolana", "Arepas"],
    "discount": {
      "id": "disc010",
      "percentage": 0,
      "startDate": None,
      "endDate": None
    },
    "rating": 4.6,
    "totalRating": 90,
    "totalReviews": 25,
    "paginationKey": "page1",
    "createdAt": "2025-02-09T16:00:00Z",
    "updatedAt": "2025-02-20T10:45:00Z"
  },
  {
    "id": "prod011",
    "name": "Falafel con Hummus",
    "description": "Croquetas de garbanzo acompañadas de hummus y pan pita.",
    "image": "https://example.com/images/falafel_hummus.jpg",
    "price": 100,
    "available": True,
    "store": {
      "id": "store009",
      "name": "Mediterráneo Express"
    },
    "category": ["Mediterránea", "Vegana"],
    "discount": {
      "id": "disc011",
      "percentage": 8,
      "startDate": "2025-02-24T00:00:00Z",
      "endDate": "2025-03-05T23:59:59Z"
    },
    "rating": 4.4,
    "totalRating": 85,
    "totalReviews": 20,
    "paginationKey": "page1",
    "createdAt": "2025-02-11T14:00:00Z",
    "updatedAt": "2025-02-20T12:00:00Z"
  },
  {
    "id": "prod012",
    "name": "Empanadas Argentinas",
    "description": "Empanadas horneadas rellenas de carne, cebolla y aceitunas.",
    "image": "https://example.com/images/empanadas_argentinas.jpg",
    "price": 75,
    "available": True,
    "store": {
      "id": "store010",
      "name": "La Casa del Asado"
    },
    "category": ["Argentina", "Snacks"],
    "discount": {
      "id": "disc012",
      "percentage": 10,
      "startDate": "2025-02-19T00:00:00Z",
      "endDate": "2025-02-27T23:59:59Z"
    },
    "rating": 4.7,
    "totalRating": 100,
    "totalReviews": 30,
    "paginationKey": "page1",
    "createdAt": "2025-02-08T11:00:00Z",
    "updatedAt": "2025-02-20T09:15:00Z"
  },
  {
    "id": "prod013",
    "name": "Pho Vietnamita",
    "description": "Sopa vietnamita con fideos de arroz, carne y hierbas frescas.",
    "image": "https://example.com/images/pho_vietnamita.jpg",
    "price": 160,
    "available": True,
    "store": {
      "id": "store011",
      "name": "Saigón Delights"
    },
    "category": ["Vietnamita", "Sopas"],
    "discount": {
      "id": "disc013",
      "percentage": 5,
      "startDate": "2025-02-22T00:00:00Z",
      "endDate": "2025-03-04T23:59:59Z"
    },
    "rating": 4.6,
    "totalRating": 120,
    "totalReviews": 35,
    "paginationKey": "page1",
    "createdAt": "2025-02-12T10:00:00Z",
    "updatedAt": "2025-02-20T08:45:00Z"
  },
  {
    "id": "prod014",
    "name": "Ceviche Peruano",
    "description": "Pescado fresco marinado en jugo de limón con cebolla y cilantro.",
    "image": "https://example.com/images/ceviche_peruano.jpg",
    "price": 170,
    "available": False,
    "store": {
      "id": "store012",
      "name": "Sabores del Perú"
    },
    "category": ["Peruana", "Mariscos"],
    "discount": {
      "id": "disc014",
      "percentage": 0,
      "startDate": None,
      "endDate": None
    },
    "rating": 4.9,
    "totalRating": 210,
    "totalReviews": 70,
    "paginationKey": "page1",
    "createdAt": "2025-02-06T12:00:00Z",
    "updatedAt": "2025-02-19T15:00:00Z"
  },
  {
    "id": "prod015",
    "name": "Croissant de Chocolate",
    "description": "Crujiente croissant relleno de chocolate derretido.",
    "image": "https://example.com/images/croissant_chocolate.jpg",
    "price": 60,
    "available": True,
    "store": {
      "id": "store013",
      "name": "Panadería Parisienne"
    },
    "category": ["Francesa", "Postres"],
    "discount": {
      "id": "disc015",
      "percentage": 7,
      "startDate": "2025-02-20T00:00:00Z",
      "endDate": "2025-02-29T23:59:59Z"
    },
    "rating": 4.5,
    "totalRating": 150,
    "totalReviews": 45,
    "paginationKey": "page1",
    "createdAt": "2025-02-13T09:00:00Z",
    "updatedAt": "2025-02-20T11:00:00Z"
  }
]

tiendas = [
  {
    "id": "1",
    "name": "La Casa de la Pizza",
    "description": "Especialistas en pizzas artesanales con ingredientes frescos.",
    "email": "contacto@lacasadelapizza.com",
    "image": "https://example.com/pizza.jpg",
    "phoneNumber": "+34 678 123 456",
    "rating": 4.8,
    "totalRating": 1200,
    "totalReviews": 250,
    "userId": "user_001",
    "paginationKey": "key_001",
    "updatedAt": "2025-03-05T12:00:00Z",
    "createdAt": "2022-07-12T08:30:00Z",
    "startTime": "2025-03-05T11:00:00Z",
    "endTime": "2025-03-05T23:00:00Z"
  },
  {
    "id": "2",
    "name": "Hamburguesas El Toro",
    "description": "Jugosas hamburguesas con carne 100% Angus y pan artesanal.",
    "email": "info@eltoro.com",
    "image": "https://example.com/burger.jpg",
    "phoneNumber": "+34 645 789 321",
    "rating": 4.7,
    "totalRating": 950,
    "totalReviews": 180,
    "userId": "user_002",
    "paginationKey": "key_002",
    "updatedAt": "2025-03-05T13:15:00Z",
    "createdAt": "2021-09-20T14:45:00Z",
    "startTime": "2025-03-05T12:00:00Z",
    "endTime": "2025-03-05T23:30:00Z"
  },
  {
    "id": "3",
    "name": "Tacos La Esquina",
    "description": "Auténticos tacos mexicanos con recetas tradicionales.",
    "email": "pedidos@tacoslaesquina.com",
    "image": "https://example.com/tacos.jpg",
    "phoneNumber": "+34 654 321 987",
    "rating": 4.9,
    "totalRating": 1100,
    "totalReviews": 275,
    "userId": "user_003",
    "paginationKey": "key_003",
    "updatedAt": "2025-03-05T14:30:00Z",
    "createdAt": "2020-05-10T09:15:00Z",
    "startTime": "2025-03-05T10:30:00Z",
    "endTime": "2025-03-05T22:00:00Z"
  },
  {
    "id": "4",
    "name": "Pastelería Dulce Encanto",
    "description": "Deliciosos pasteles, tartas y postres caseros.",
    "email": "info@dulceencanto.com",
    "image": "https://example.com/pasteleria.jpg",
    "phoneNumber": "+34 612 345 678",
    "rating": 4.6,
    "totalRating": 800,
    "totalReviews": 150,
    "userId": "user_004",
    "paginationKey": "key_004",
    "updatedAt": "2025-03-05T11:45:00Z",
    "createdAt": "2019-03-08T07:30:00Z",
    "startTime": "2025-03-05T08:00:00Z",
    "endTime": "2025-03-05T20:00:00Z"
  },
  {
    "id": "5",
    "name": "Sushi Express",
    "description": "El mejor sushi a domicilio, calidad y frescura garantizadas.",
    "email": "reservas@sushiexpress.com",
    "image": "https://example.com/sushi.jpg",
    "phoneNumber": "+34 600 789 456",
    "rating": 4.8,
    "totalRating": 1250,
    "totalReviews": 300,
    "userId": "user_005",
    "paginationKey": "key_005",
    "updatedAt": "2025-03-05T15:10:00Z",
    "createdAt": "2021-12-15T10:00:00Z",
    "startTime": "2025-03-05T11:00:00Z",
    "endTime": "2025-03-05T22:30:00Z"
  },
  {
    "id": "6",
    "name": "Café Aromático",
    "description": "Café de especialidad con granos seleccionados.",
    "email": "contacto@cafearomatico.com",
    "image": "https://example.com/cafe.jpg",
    "phoneNumber": "+34 630 123 987",
    "rating": 4.9,
    "totalRating": 1350,
    "totalReviews": 400,
    "userId": "user_006",
    "paginationKey": "key_006",
    "updatedAt": "2025-03-05T09:00:00Z",
    "createdAt": "2018-10-05T08:20:00Z",
    "startTime": "2025-03-05T07:00:00Z",
    "endTime": "2025-03-05T19:00:00Z"
  },
  {
    "id": "7",
    "name": "Asador El Gaucho",
    "description": "Carnes a la parrilla con el auténtico sabor argentino.",
    "email": "reservas@elgaucho.com",
    "image": "https://example.com/asador.jpg",
    "phoneNumber": "+34 611 654 321",
    "rating": 4.7,
    "totalRating": 980,
    "totalReviews": 220,
    "userId": "user_007",
    "paginationKey": "key_007",
    "updatedAt": "2025-03-05T16:00:00Z",
    "createdAt": "2020-02-17T11:10:00Z",
    "startTime": "2025-03-05T12:30:00Z",
    "endTime": "2025-03-05T23:00:00Z"
  },
  {
    "id": "8",
    "name": "Panadería La Tradición",
    "description": "Pan recién horneado con recetas tradicionales.",
    "email": "info@latradicion.com",
    "image": "https://example.com/panaderia.jpg",
    "phoneNumber": "+34 609 876 543",
    "rating": 4.8,
    "totalRating": 890,
    "totalReviews": 210,
    "userId": "user_008",
    "paginationKey": "key_008",
    "updatedAt": "2025-03-05T07:30:00Z",
    "createdAt": "2017-06-01T06:45:00Z",
    "startTime": "2025-03-05T06:00:00Z",
    "endTime": "2025-03-05T18:00:00Z"
  },
  {
    "id": "9",
    "name": "Mariscos del Pacífico",
    "description": "Pescados y mariscos frescos, directo del mar a tu mesa.",
    "email": "contacto@mariscospacifico.com",
    "image": "https://example.com/mariscos.jpg",
    "phoneNumber": "+34 690 432 876",
    "rating": 4.8,
    "totalRating": 1100,
    "totalReviews": 270,
    "userId": "user_009",
    "paginationKey": "key_009",
    "updatedAt": "2025-03-05T12:45:00Z",
    "createdAt": "2019-11-20T10:00:00Z",
    "startTime": "2025-03-05T12:00:00Z",
    "endTime": "2025-03-05T22:00:00Z"
  },
  {
    "id": "10",
    "name": "Veggie Delight",
    "description": "Comida 100% vegetariana y vegana con ingredientes orgánicos.",
    "email": "info@veggiedelight.com",
    "image": "https://example.com/veggie.jpg",
    "phoneNumber": "+34 677 908 345",
    "rating": 4.9,
    "totalRating": 1400,
    "totalReviews": 320,
    "userId": "user_010",
    "paginationKey": "key_010",
    "updatedAt": "2025-03-05T13:30:00Z",
    "createdAt": "2020-08-15T09:30:00Z",
    "startTime": "2025-03-05T10:00:00Z",
    "endTime": "2025-03-05T21:00:00Z"
  },
  {
    "id": "11",
    "name": "El Rincón del Pollo",
    "description": "Pollo asado con recetas especiales y salsas caseras.",
    "email": "pedidos@rincondelpollo.com",
    "image": "https://example.com/pollo.jpg",
    "phoneNumber": "+34 622 567 890",
    "rating": 4.7,
    "totalRating": 980,
    "totalReviews": 250,
    "userId": "user_011",
    "paginationKey": "key_011",
    "updatedAt": "2025-03-05T14:00:00Z",
    "createdAt": "2021-06-22T11:15:00Z",
    "startTime": "2025-03-05T11:30:00Z",
    "endTime": "2025-03-05T22:30:00Z"
  },
  {
    "id": "12",
    "name": "Bodega Española",
    "description": "Tapas y vinos de las mejores regiones de España.",
    "email": "contacto@bodegaespanola.com",
    "image": "https://example.com/tapas.jpg",
    "phoneNumber": "+34 633 321 654",
    "rating": 4.8,
    "totalRating": 1200,
    "totalReviews": 280,
    "userId": "user_012",
    "paginationKey": "key_012",
    "updatedAt": "2025-03-05T17:00:00Z",
    "createdAt": "2018-04-10T10:45:00Z",
    "startTime": "2025-03-05T13:00:00Z",
    "endTime": "2025-03-05T23:30:00Z"
  },
  {
    "id": "13",
    "name": "Heladería Frescura",
    "description": "Helados artesanales con ingredientes naturales y sabores únicos.",
    "email": "info@heladeriafrescura.com",
    "image": "https://example.com/helado.jpg",
    "phoneNumber": "+34 699 876 543",
    "rating": 4.9,
    "totalRating": 1300,
    "totalReviews": 330,
    "userId": "user_013",
    "paginationKey": "key_013",
    "updatedAt": "2025-03-05T18:30:00Z",
    "createdAt": "2019-09-05T12:20:00Z",
    "startTime": "2025-03-05T10:00:00Z",
    "endTime": "2025-03-05T22:00:00Z"
  },
  {
    "id": "14",
    "name": "Pasta Bella",
    "description": "Auténtica comida italiana con pasta hecha a mano.",
    "email": "reservas@pastabella.com",
    "image": "https://example.com/pasta.jpg",
    "phoneNumber": "+34 655 234 987",
    "rating": 4.8,
    "totalRating": 1150,
    "totalReviews": 290,
    "userId": "user_014",
    "paginationKey": "key_014",
    "updatedAt": "2025-03-05T19:00:00Z",
    "createdAt": "2020-01-30T15:00:00Z",
    "startTime": "2025-03-05T12:00:00Z",
    "endTime": "2025-03-05T23:00:00Z"
  },
  {
    "id": "15",
    "name": "Donas & Café",
    "description": "Donas recién hechas y café gourmet para acompañarlas.",
    "email": "contacto@donasycafe.com",
    "image": "https://example.com/donas.jpg",
    "phoneNumber": "+34 611 678 234",
    "rating": 4.7,
    "totalRating": 950,
    "totalReviews": 260,
    "userId": "user_015",
    "paginationKey": "key_015",
    "updatedAt": "2025-03-05T20:15:00Z",
    "createdAt": "2019-07-18T13:10:00Z",
    "startTime": "2025-03-05T08:00:00Z",
    "endTime": "2025-03-05T20:00:00Z"
  }
]


def insertar_productos():
    for producto in productos:
        doc_ref = db.collection('products').document(producto['id'])
        doc_ref.set(producto)


def insertar_tiendas():
    for tienda in tiendas:
        doc_ref = db.collection('stores').document(tienda['id'])
        doc_ref.set(tienda)


def main():
    insertar_productos()
    insertar_tiendas()


if __name__ == "__main__":
    main()