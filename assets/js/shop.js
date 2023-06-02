





const products = [
  { id: "veg", name: 'Souper Fresh Veg', price: 3.00 },
  { id: "daru", name: 'Daru', price: 5.00 },
  { id: "orchard", name: 'Tipperary Orchard', price: 5.00 },
  {id:"gleann oir",name:'Gleann Oir',price:5.00}
];


const cart = [];


function addToCart(productId) {
  const product = products.find((item) => item.id === productId);
  
  if (product) {
    cart.push(product);
    console.log('Item added to cart:', product);
    console.log(cart)
  }
}

