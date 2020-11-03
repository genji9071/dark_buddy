import React, { useEffect } from "react";
import { WhiteSpace, Result, Icon } from "antd-mobile";
import useQuery from "hooks/useQuery";
import getUser from "utils/getUser";

export default () => {
  const icon = useQuery("icon");
  const title = useQuery("title");
  const message = useQuery("message");
  useEffect(() => {
    async function run() {
      const user = await getUser();
      console.log(user);
    }
    run();
  }, [])
  return (
    <div>
      <WhiteSpace size="lg" />
      <Result
        img={icon && <Icon type={icon} size="lg" style={{ fill: "#1F90E6" }} />}
        title={title}
        message={message}
      />
    </div>
  )
}
