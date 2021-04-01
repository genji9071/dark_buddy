import React from "react";
import "../../styles/feedcard.scss"

const FeedCard = ({ feedName, feedCreator }) => {
  return (
    <div>
      <div className="names">
        <div className="feed">{feedName}</div>
        <div className="creator">{feedCreator}</div>
      </div>
    </div>
  );
};

export default FeedCard;
