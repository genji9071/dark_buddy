import React from 'react';

const state = (n) => {return n};

var sleep = (n) => {
    const s = Date.now();
    while (Date.now() < s + n) {}
};

var x = state(0);

x(0);

console.log('first x', x());

var y = state(() => {
    sleep(1000);
    return x() + 1;
});
var z = state(() => [x(), y(), x() + y()]);

x(1);

console.log('second x', x());
console.log('second y', y());
console.log('second z', z());

x(10)

console.log('third x', x());
console.log('third y', y());
console.log('third z', z());
