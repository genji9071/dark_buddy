import { useLocation } from "react-router";
import { useMemo } from "react";

export default (name: string) => {
  const location = useLocation();
  const value = useMemo(() => {
    const search = new URLSearchParams(location.search);
    return search.get(name);
  }, [location, name]);
  return value;
}