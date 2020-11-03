import { useContext } from "react";
import { RouteComponentProps, StaticContext } from "react-router";
import { LocationState } from "history";
//@ts-ignore
import { __RouterContext as RouterContext } from "react-router";

// FIXME:  use official API when https://github.com/ReactTraining/react-router/pull/6453 merged

/**
 * 获取路由信息
 */
export function useRouter<
  Params extends { [K in keyof Params]?: string } = {},
  C extends StaticContext = StaticContext,
  S = LocationState
>() {
  return useContext(RouterContext) as RouteComponentProps<Params, C, S>;
}
