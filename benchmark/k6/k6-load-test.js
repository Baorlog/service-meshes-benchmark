import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
    stages: [
        { duration: '10s', target: 20 }, // Ramp up to 10 usersahihu
        { duration: '30s', target: 20 }, // Stay at 10 users
        { duration: '10s', target: 0 },  // Ramp down to 0 users
    ],
};

export default function () {
    http.get('http://192.168.49.2:32385/');
    sleep(1);
}
