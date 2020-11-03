import axios from "axios";
import getUser from "./getUser";

export interface IDarkspyWord {
  name: string
  word: string
}

export default async function (chatbotUserId: string) {
  const user = await getUser();
  const res = await axios.post<IDarkspyWord>(
    `/dark_buddy/darkSpy/getWord`,
    { chatbotUserId, name: user.nickName }
  );
  return res.data;
}