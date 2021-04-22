import React from "react";
import "./styles/Card_3.scss"

const Card_3 = ({ cardData }) => {
  // console.log(props);
  return (
    <div className="main">
      <div className="profile">
        <img src={cardData.user.profileImage} alt={""} />
        <div className="text">
          <h1>{cardData.user.name}</h1>
          <h3>"CARD3.COMPANY"</h3>
          <p className="design">"CARD3.DESIGN"</p>
        </div>
      </div>
      <div className="below">
        <p className="usual">"CARD3.COLLABORATION"</p>
        <p className="pics">
          {cardData.user.collaboratedWith.map(data => (
            <img src={data.profileImage} alt={""} />
          ))}
        </p>
      </div>
      <div className="btn">
        <a href="#" className="fa fa-linkedin" />

        <a href="#" className="fa fa-dribbble" />

        <a href="#" className="fa fa-twitter" />
      </div>
    </div>
  );
};

export default Card_3;
