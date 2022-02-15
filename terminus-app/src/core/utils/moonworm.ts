// interface ABIGeneric<T> {
//   new (): T;
// }

import { AbiItem } from "web3-utils";
// demo:
class ABIGeneric {
  constructor() {}
}

const extendClass = (abiItems: Array<AbiItem>) => () => {
  const o = new ABIGeneric();
  for (var i = 0; i < abiItems.length; i++) {
    const methodName: keyof ABIGeneric = abiItems[i].name ?? "_";
    const method = (x: number) => x + 1;
    if (methodName) {
      o[methodName] = method; // type sig seems unnecessary
    }
  }
  return o;
};

const extHelloConstr = extendClass(ABIGeneric, {
  incr: (x: number) => x + 1,
  show: (n: number) => "nr " + n,
});
const extHello = extHelloConstr("jimmy");

extHello.hello();
const test1 = extHello.incr(1);
const test2 = extHello.show(42);
const test3 = extHello.hello();
console.log(test1, test2, test3);

export default generateClass;
