import React from "react";
import "../../styles/card1.scss"

const Card_1 = ({ cardData }) => {
  const onClickListener = () => {
    return cardData.messageLink
  }
  return (
    <div className="all">
      <div className="image">
        <img src={cardData.image}/>
        <div className="content1" >
          <a className="fa fa-map-marker" href={cardData.messageLink} />
          {cardData.heading}
        </div>
      </div>
    </div>
  );
};

export default Card_1;
