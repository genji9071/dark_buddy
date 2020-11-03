import React, { ComponentType } from "react";
import { Route, Redirect, RouteProps } from "react-router";
import localStorage from "utils/localStorage";
import { ROOT_PATH } from "config";

/**
 * 用于登陆验证的路由组件
 * @param props 
 */
export function PrivateRoute(props: RouteProps & { component: ComponentType }) {
  const { component: Component, ...rest } = props;
  return (
    <Route
      {...rest}
      render={props =>
        localStorage.get("sender_id") ?
          <Component {...props} /> :
          <Redirect to={{
            pathname: `${ROOT_PATH}/result`,
            search: `title=未绑定账号&message=请通过钉钉对话框向暗黑群发送[@暗黑小哥 **注册]来绑定账号`,
            state: { from: props.location }
          }} />
      }
    />
  );
}