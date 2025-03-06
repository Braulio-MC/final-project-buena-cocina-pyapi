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

def insertar_productos():
    for producto in productos:
        doc_ref = db.collection('productos').document(producto['id'])
        doc_ref.set(producto)


if __name__ == "__main__":
    insertar_productos()