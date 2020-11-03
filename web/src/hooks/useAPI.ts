import { useState, useEffect, DependencyList, useCallback } from "react";
import axios, { AxiosRequestConfig } from "axios";

/**
 * 调用接口
 */
export default <T>(
  url: string,
  option: AxiosRequestConfig = { method: "GET" },
  deps: DependencyList = []
): [{ data: T | undefined; loading: boolean; err: any; count: number }, () => void] => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<T>();
  const [err, setErr] = useState();
  const [count, setCount] = useState(0);
  const refetch = useCallback(() => setCount(n => n + 1), [setCount]);
  useEffect(() => {
    setLoading(true);
    axios.request<T>({ url, ...option })
      .then(res => setData(res.data))
      .catch(e => setErr(e))
      .finally(() => setLoading(false));
  }, [count, ...deps]);
  return [{ data, loading, err, count }, refetch];
};
