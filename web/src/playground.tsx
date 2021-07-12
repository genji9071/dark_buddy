import React, { memo, useEffect, useMemo, useRef, useState } from 'react';
import { render } from 'react-dom';

import { action, autorun, computed, observable, reaction, runInAction, toJS, when } from 'mobx';
import { setInterval } from 'timers';

import { produce } from 'immer';

// * ================================================================================

// const data = { countObj: { value: 0 }, date: { value: new Date() } };

// const prevObj = {
//   a: {
//     b: { c: { d: 1 } },
//     b2: { s: 2 },
//   },
//   s: { s: 'value' },
// };

// const nextObj = produce(prevObj, (obj) => {
//   obj.a.b.c.d += 1;
// });

// // @ts-ignore
// window.arr = [prevObj, nextObj];

// console.log(
//   'lcdebug e58ad3',
//   //
//   prevObj === nextObj,
//   prevObj.s === nextObj.s,
//   prevObj.a === nextObj.a,
//   prevObj.a.b2 === nextObj.a.b2,
// );

// const status = observable({ panel: 'font', statusCount: 0 });

// const mycomputed = computed(() => {
//   if (status.panel !== 'font') {
//     return data.countObj.value;
//   } else {
//     return Infinity;
//   }
// });

// // @ts-ignore
// window.arr = [];
// autorun((arg) => {
//   // console.log('lcdebug ba39b3', obj.s);
//   console.log('lcdebug ba39b3', obj, obj.a.b);

//   // @ts-ignore
//   window.arr.push(obj);
// });

// runInAction(() => {
//   // obj.a.b.c.d += 1;
//   obj.a = { b: { c: { d: 1 } } };

//   // console.log('lcdebug 37c87d', obj);
// });

function App() {
  return <div></div>
}

render(<App />, document.getElementById('root'));

// * ================================================================================

// import { BehaviorSubject, Subject } from 'rxjs';

// const d$ = new BehaviorSubject(1000);
// const e$ = new BehaviorSubject(1);

// export const Comp2: FC<{ k: number }> = memo(({ k }) => {
//   // const mapperRef = useRef(mapper!);
//   // // @ts-ignore 这两行懒得做类型了，整体表现是正常的
//   // mapperRef.current = mapper ?? ((e: T) => e);

//   // const [result, setResult] = useState(() => mapperRef.current(store.getState()));
//   // const lastResult = useRef(result);

//   // useEffect(() => {
//   //   return store.subscribe((state) => {
//   //     const nextResult = mapperRef.current(state);

//   //     // * 性能：仅进行快速比较，如果要进行深度比较，自行处理 mapper 函数的返回值
//   //     if (nextResult === lastResult.current) return;

//   //     lastResult.current = nextResult;
//   //     setResult(nextResult);
//   //   });
//   // }, []);

//   const [tick, setTick] = useState(1000);

//   useEffect(() => {
//     let count = 0;
//     d$.subscribe(() => {
//       count += 1;
//       // console.log('lcdebug 548b7d', count);
//     });

//     e$.subscribe(() => {
//       count += 1;
//       // console.log('lcdebug a63908', count);
//     });

//     setInterval(() => {
//       d$.next(d$.value + 1000);
//       e$.next(e$.value + 1);
//       // console.log('lcdebug b38c76', count, d$.value + e$.value);
//       Promise.resolve().then(() => {
//         if (count === 0) return;
//         setTick(d$.value + e$.value);
//         count = 0;
//       });
//     }, 1000);
//   }, []);

//   console.log('lcdebug aa3df5', tick);

//   // * ----------------

//   return (
//     <>
//       <div>~{}~</div>
//     </>
//   );
// });

// export const App2: FC = () => {
//   const [tick, setTick] = useState(0);
//   useEffect(() => {
//     setInterval(() => {
//       setTick((tick) => tick + 1);
//     }, 1000);
//   }, []);

//   return (
//     <>
//       <div>
//         <Comp2></Comp2>
//       </div>
//     </>
//   );
// };

// render(<App2 />, document.getElementById('root'));

// * ================================================================================