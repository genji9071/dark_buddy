import React, { useEffect, useState } from 'react'
import { Result } from 'antd-mobile'
import getDarkspyWord, { IDarkspyWord } from 'utils/getDarkspyWord';
import useQuery from 'hooks/useQuery';

export default () => {
  const chatbotUserId = useQuery("chatbotUserId");
  const [data, setData] = useState<IDarkspyWord>();
  useEffect(() => {
    chatbotUserId && getDarkspyWord(chatbotUserId).then(setData);
  }, [chatbotUserId]);
  return (
    <div>
      {data &&
        <Result
          message={`${data.name}，你领到的词是【${data.word}】`}
        />
      }
    </div>
  )
}
