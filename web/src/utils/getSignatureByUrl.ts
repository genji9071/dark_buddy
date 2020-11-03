import axios from "axios";

export interface ISignature {
  agentId: string;
  corpId: string;
  nonceStr: string;
  signature: string;
  timeStamp: string;
}

export default async function (url: string) {
  const { data } = await axios.post<ISignature>(`/dark_buddy/sign_in/get_signature_by_url?t=${Date.now()}`, { url });
  return data;
}