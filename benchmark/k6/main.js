import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10, // Số lượng Virtual Users
//   duration: '30s', 
//   duration: '1h', 
  duration: '30h', 
};

export default function () {
  const res = http.get('http://192.168.1.6:8000');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
