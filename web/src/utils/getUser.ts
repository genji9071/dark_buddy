import dingtalk from "dingtalk-jsapi"
import getSignatureByUrl from "./getSignatureByUrl";

export interface IUser {
  avatar: string;
  corpId: string;
  emplId: string;
  id: string;
  isAuth: true
  isManager: false
  nickName: string;
  rightLevel: number;
}

export default async function () {
  const signature = await getSignatureByUrl(window.location.href);
  await dingtalk.config({ ...signature, type: 0, jsApiList: ["biz.user.get"] });
  const user = await dingtalk.biz.user.get({});
  return user as IUser;
}