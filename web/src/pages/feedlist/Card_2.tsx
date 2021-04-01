import React from "react";
import "./styles/Card_2.scss"

const Card_2 = ({ cardData }) => {
  return (
    <div className="container">
      <img src={cardData.bannerImage} alt={""} />
      <div className="content">
        <p className="heading">"CARD2.HEADLINE"</p>
        <p className="brief">"CARD2.BRIEF"</p>
        <p className="detail">"CARD2.DETAILS"</p>
      </div>
    </div>
  );
};

export default Card_2;
