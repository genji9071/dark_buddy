import store from "store";

export interface Store {
  session_id: string;
}

export default {
  get(key: keyof Store) {
    return store.get(key)
  },
  set<K extends keyof Store>(key: K, value: Store[K]) {
    store.set(key, value);
  }
}