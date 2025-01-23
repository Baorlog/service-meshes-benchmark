export let options = {
    scenarios: {
      constant_load: {
        executor: 'constant-vus',
        vus: 50,
        duration: '1m',
      },
      ramping_load: {
        executor: 'ramping-vus',
        startVUs: 0,
        stages: [
          { duration: '30s', target: 50 },
          { duration: '30s', target: 0 },
        ],
      },
    },
  };
  

const url = 'http://example.com/api';
const payload = JSON.stringify({ name: 'Test', age: 30 });

const headers = { 'Content-Type': 'application/json' };
const res = http.post(url, payload, { headers });
  