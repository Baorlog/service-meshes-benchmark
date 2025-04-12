import http from 'k6/http';
import { sleep, group } from 'k6';

export const options = {}; // all defined via CLI

const BASE_URL = __ENV.FRONTEND_URL || 'http://localhost:3000'; // fallback

export default function () {
  // Same Online Boutique user flow as before
  group('Visit homepage', () => {
    http.get(`${BASE_URL}/`);
    sleep(1);
  });
  group('Change currency', () => {
    http.get(`${BASE_URL}/setCurrency?currencyCode=EUR`);
    sleep(1);
  });
  group('Browse products', () => {
    http.get(`${BASE_URL}/products`);
    sleep(2);
  });
  group('View a product', () => {
    http.get(`${BASE_URL}/product/OLJCESPC7Z`);
    sleep(1);
  });
  group('Add to cart', () => {
    http.post(`${BASE_URL}/cart`, JSON.stringify({
      productId: 'OLJCESPC7Z',
      quantity: 1,
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
    sleep(1);
  });
  group('View cart', () => {
    http.get(`${BASE_URL}/cart`);
    sleep(1);
  });
  group('Checkout', () => {
    http.post(`${BASE_URL}/checkout`, JSON.stringify({
      user: 'testuser',
      address: '123 k6 Street',
      payment: 'VISA',
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
    sleep(2);
  });
}
